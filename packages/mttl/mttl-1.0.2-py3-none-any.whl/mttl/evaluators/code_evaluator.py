import os

import tqdm
from evaluate import load

from mttl.evaluators.base import GenerativeEvaluator, switch_to_eval_mode
from mttl.logging import logger
import csv


# reference: https://github.com/declare-lab/instruct-eval/blob/main/human_eval/main.py#L35
def count_indent(text: str) -> int:
    count = 0
    for char in text:
        if char == " ":
            count += 1
        else:
            break
    return count


def fix_indents(text: str, multiple: int = 2):
    outputs = []
    for line in text.split("\n"):
        while count_indent(line) % multiple != 0:
            line = " " + line
        outputs.append(line)
    return "\n".join(outputs)


def filter_code(completion: str) -> str:
    # The program tends to overwrite, we only take the first function
    completion = completion.lstrip("\n")
    return completion.split("\n\n")[0]

def combine_testcase(test):
    tests = test.split("\n")
    tests = [test.replace("assert", "") for test in tests]
    new_test = "assert (" + ") and (".join(tests) + ")"
    return new_test
    
class CodeEvaluator(GenerativeEvaluator):
    def __init__(
        self,
        datamodule,
        use_vllm=False,
        generation_kwargs=None,
        prepend_source=True,
        split="test",
    ):
        super().__init__(
            datamodule=datamodule,
            use_vllm=use_vllm,
            generation_kwargs=generation_kwargs,
        )

        self.split = split
        self.prepend_source = prepend_source
        os.environ["HF_ALLOW_CODE_EVAL"] = "1"

    @switch_to_eval_mode
    def evaluate(
        self,
        model,
        split=None,
        subsample=-1,
        num_batches=None,
        verbose=True,
        shuffle=False,
        output_path=None,
        **kwargs,
    ):
        dataloader = self.get_dataloader(
            split or self.split, subsample, shuffle=shuffle
        )

        if self.use_vllm:
            return self.evaluate_with_vllm(model, dataloader, num_batches, verbose)

        pbar = tqdm.tqdm(
            enumerate(dataloader),
            total=len(dataloader),
        )

        all_predictions = []

        all_references = []
        all_sources_texts = []
        all_tests = []

        metric = load("code_eval")
        metric_test = load("code_eval")
        for num_batch, batch in pbar:
            # we assume code prefixes are available and these are "completion" tasks
            sources_texts = batch.pop("code_prefix")
            tests = batch.pop("code_tests")

            predictions = self.generate_for_batch(model, batch)
            generated = list(
                map(
                    lambda x: filter_code(fix_indents(x)),
                    predictions.generated_texts,
                )
            )
            predictions = [
                [(s if self.prepend_source else "") + p]
                for s, p in zip(
                    sources_texts,
                    generated,  
                )
            ]

            if verbose:
                logger.info("Prediction:")
                logger.info(predictions[0][0])

            rows = zip(predictions, tests, sources_texts)
            for p, t, s in list(rows):
                t = combine_testcase(t)
                metrics_1, _ = metric_test.compute(predictions=[p], references=[t], k=[1])
                all_references.append(metrics_1["pass@1"])
                all_sources_texts.append(s)
                all_tests.append(t)
                

            all_predictions.extend([p[0] for p in predictions])
            
            
            
            metric.add_batch(predictions=predictions, references=tests)

            if num_batches is not None and num_batch >= num_batches:
                break
                
        rows = zip(all_sources_texts, all_references, all_predictions, all_tests)
        with open(os.path.join(output_path, 'task_output.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Questions', 'Answer', 'Prediction', 'Tests'])  # Write header
            writer.writerows(rows)
        
        metrics, _ = metric.compute(k=[1])

        self.save_metrics(metrics, output_path, predictions=all_predictions)
        return metrics["pass@1"]
