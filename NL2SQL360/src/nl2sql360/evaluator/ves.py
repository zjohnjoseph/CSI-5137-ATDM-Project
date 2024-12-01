from .bird_eval.bird_ves import run_sqls_parallel, sort_results
import os
import math
from loguru import logger


class VesEvaluator:
    
    def __init__(self, reuse_ex, sql_dialect="SQLite", **kwds):
        self.reuse_ex = reuse_ex
        self.sql_dialect = sql_dialect
        self.db_host = kwds.get("db_host", None)
        self.db_port = kwds.get("db_port", None)
        self.db_name = kwds.get("db_name", None)
        self.user = kwds.get("db_user", None)
        self.password = kwds.get("db_password", None)
        
    
    def evaluate(self, gold_sqls, pred_sqls, db_ids, db_dir, **kwds):
        query_pairs = list(zip(pred_sqls, gold_sqls))
        db_places = [os.path.join(db_dir, db_id, f"{db_id}.sqlite") for db_id in db_ids]
        exec_acc_list = kwds.get("exec_acc_list", None)
        if self.reuse_ex and exec_acc_list is None:
            logger.warning("VES evaluator is set to reuse the EX result, but it has not been passed in.")
        ves_result = run_sqls_parallel(
            sqls=query_pairs,
            db_places=db_places,
            num_cpus=kwds.get("num_processes", 8),
            meta_time_out=kwds.get("timeout", 30),
            exec_acc_list=exec_acc_list,
            sql_dialect=self.sql_dialect,
            host=self.db_host,
            user=self.user,
            password=self.password,
            dbname=self.db_name,
            port=self.db_port
        )
        ves_result = sort_results(ves_result)
        ves_result = [math.sqrt(res['time_ratio']) for res in ves_result]
        return {
            "ves": ves_result
        }
    
    def get_eval_metrics(self):
        return ["ves"]
