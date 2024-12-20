import numpy as np
import torch
import tqdm
import csv
import os

from mttl.evaluators.base import Evaluator, switch_to_eval_mode
from mttl.logging import logger
from mttl.models.utils import compute_loglike_loss


class LogLikeEvaluator(Evaluator):
    def __init__(self, datamodule, **kwargs):
        super().__init__(datamodule=datamodule, **kwargs)

    @switch_to_eval_mode
    def evaluate(
        self,
        model,
        split="val",
        subsample=-1,
        num_batches=None,
        verbose=True,
        shuffle=False,
        output_path=None,
    ):
        from mttl.models.expert_model import BaseExpertModel
        from mttl.models.lightning.base_module import LightningEfficientCheckpoint
        from mttl.models.utils import transfer_batch_to_device

        dataloader = self.get_dataloader(split, subsample, shuffle=shuffle)

        if self.use_vllm:
            return self.evaluate_with_vllm(model, dataloader, num_batches, verbose)

        pbar = tqdm.tqdm(
            enumerate(dataloader),
            total=len(dataloader),
        )

        all_losses = []
        all_accuracies = []
        all_predictions = []
        
        all_references = []
        all_sources_texts = []
        all_task_names = []

        device = next(model.parameters()).device

        for num_batch, batch in pbar:
            if num_batches is not None and num_batch >= num_batches:
                break
            labels_index = batch.pop("labels_index", None)
            num_options = batch.pop("num_options")
            labels_texts = batch.pop("labels_texts")
            sources_texts = batch.pop("sources_texts")
            task_names = batch.pop("id_task")
            batch_size = len(labels_index)

            batch = transfer_batch_to_device(batch, device)

            with torch.no_grad():
                if isinstance(model, LightningEfficientCheckpoint) or isinstance(
                    model, BaseExpertModel
                ):
                    logits = model.forward(**batch).logits
                else:
                    logits = model.forward(
                        input_ids=batch["input_ids"],
                        attention_mask=batch["attention_mask"],
                    ).logits

                loss_per_option = compute_loglike_loss(
                    logits, batch["labels"], reduction="none"
                )
                #loss_per_option = loss_per_option.cpu().numpy()
                loss_per_option = loss_per_option.cpu().float().numpy()
                loss_per_example = [
                    loss_per_option[
                        int(np.sum(num_options[:i])) : int(np.sum(num_options[: i + 1]))
                    ]
                    for i in range(batch_size)
                ]
                predictions = [
                    np.argmin(option_loss) for option_loss in loss_per_example
                ]

                all_predictions.extend(predictions)    
                
                all_references.extend(labels_index)
                all_sources_texts.extend(sources_texts)
                all_task_names.extend(task_names)
                
                all_losses.extend(loss_per_option.tolist())

                if labels_index is not None:
                    all_accuracies.extend(
                        (np.array(predictions) == np.array(labels_index)).tolist()
                    )

            if verbose:
                logger.info("Sources:\n%s", sources_texts[0])
                logger.info("Label:\n%s", labels_texts[labels_index[0]])
                logger.info("Prediction:\n%s", labels_texts[predictions[0]])

            if all_accuracies:
                pbar.set_description("Accuracy: {:.4f}".format(np.mean(all_accuracies)))
                
        rows = zip(all_sources_texts, all_references, all_predictions, all_task_names)
    
        # Write to CSV
        with open(os.path.join(output_path,'task_output.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Questions', 'Answer', 'Prediction', 'Task_name'])  # Write header
            writer.writerows(rows)
            
        metrics = {
            "loss": float(np.mean(all_losses)),
            "loglike": -float(np.mean(all_losses)),
            "predictions": all_predictions,
            "accuracy": float(np.mean(all_accuracies)) if all_accuracies else None,
        }

        self.save_metrics(metrics, output_path)
        return metrics["accuracy"]
