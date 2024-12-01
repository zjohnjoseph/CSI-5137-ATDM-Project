from nl2sql360.core import Core
from nl2sql360.arguments import CoreArguments, EvaluationArguments

if __name__ == "__main__":
    core_args = CoreArguments()

    core = Core(core_args)

    evaluation_args = EvaluationArguments(
        eval_name="RESDSQL-3B",
        eval_dataset="spider_dev10",
        eval_metrics=["ex","ves"],
        pred_sqls_file="../data/spider/dev_gold.sql",
        enable_spider_eval=True
    )

    core.evaluate(evaluation_args)
