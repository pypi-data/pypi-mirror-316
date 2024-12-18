from datav_server.db_factory import DatabaseFactory


def get_datav_config(user_id,mof_div_code,fiscal_year):
    db = DatabaseFactory.get_database()
    sql = f"select * from datav_task_config where exists (select 1 from datav_task_authorize  where mof_div_code = '{mof_div_code}' and fiscal_year = '{fiscal_year}' and user_id = '{user_id}')"
    configs = db.select_json_data_by_sql(sql)
    if configs:
        for temp_config in configs:
            datav_task_id = temp_config.get("datav_task_id")
            sql = f"select * from datav_task_data_sets where datav_task_id = '{datav_task_id}' and mof_div_code = '{mof_div_code}' and fiscal_year = '{fiscal_year}'"
            data_sets = db.select_json_data_by_sql(sql)
            temp_config["data_sets"] = data_sets
    return configs