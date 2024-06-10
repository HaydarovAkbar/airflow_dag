# import pendulum
# import datetime as dt
# from datetime import timedelta
#
# import md_dwh
#
# from airflow.models import DAG
# from airflow.sensors.sql import SqlSensor
# from airflow.operators.python import PythonOperator
# from airflow.operators.email_operator import EmailOperator
# from airflow.operators.python import get_current_context
# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
# from airflow.sensors.external_task_sensor import ExternalTaskSensor
# from airflow.providers.http.hooks.http import HttpHook
# from airflow.utils.task_group import TaskGroup
# from airflow.exceptions import AirflowException
#
#
# import logging
# import psycopg2
#
# local_tz = pendulum.timezone('Asia/Tashkent')
#
# #подключаемся к нужным базам (источник/приемник)
# par = md_dwh.get_dsn_parameters()
#
# SRC_SAP = HttpHook(method='POST', http_conn_id='sap_conn')
#
# default_args = {
#     'owner': 'dwh_l2_to_l2',
#     'start_date': dt.datetime(2023, 12, 22),
#     'retries': 0,
#     'email': ['b_alimov@ipakyulibank.uz'],
#     'email_on_failure': True,
#     'email_on_retry': False
# }
#
#
# def p_workflow_registration(**kwargs):
#     ti = kwargs['ti']
#     str_load_id = ti.xcom_pull(key='load_id', task_ids='get_load_id')
#     context = get_current_context()
#     dag_id = context['dag_run'].dag_id
#     task_id = context['dag_run'].run_id
#     log_url = context['task_instance'].log_url
#     md_dwh.workflow_registration(dag_id, dag_id, 'l2')
#     md_dwh.workflow_set_data_load_session(str_load_id, local_tz.convert(context['logical_date']).to_date_string(), 'l2',
#                                           'start')
#     md_dwh.workflow_set_reg_data_job_session(str_load_id, task_id, dag_id, 'start')
#     md_dwh.workflow_set_data_session_log(task_id, 'i', 'start - > task_id = ' +
#                                          task_id + ', dag_id = ' + dag_id + ', log_url = ' + log_url)
#
#
# def p_end(**kwargs):
#     ti = kwargs['ti']
#     str_load_id = ti.xcom_pull(key='load_id', task_ids='get_load_id')
#     context = get_current_context()
#     dag_id = context['dag_run'].dag_id
#     task_id = context['dag_run'].run_id
#     log_url = context['task_instance'].log_url
#     md_dwh.workflow_update_data_load_session(str_load_id, 's')
#     md_dwh.workflow_set_reg_data_job_session(str_load_id, task_id, dag_id, 's')
#     md_dwh.workflow_set_data_session_log(task_id, 'i', 'successful - > task_id = '
#                                          + task_id + ', dag_id = ' + dag_id + ', log_url = ' + log_url)
#
#
# # def p_create_dwh_flag():
# #     context = get_current_context()
# #     dag_id = context['dag_run'].dag_id
# #     md_dwh.create_dwh_flag('загрузка datasets из dwh l2 в dwh l2', 'l2_datasets_load_successful',
# #                            local_tz.convert(context['logical_date']).to_date_string(), 'l2', 'airflow',
# #                            'загрузка datasets из dwh l2 в dwh l2', dag_id)
#
#
# # отправка флага готовности в систему SAP
# def p_send_flg_to_sap(**kwargs):
#     context = get_current_context()
#
#     sql_query = f'''
#         select count(*) as count
#         from wk_export.ds_client_segmentation_last_v
#     '''
#
#     count = None
#     conn = psycopg2.connect(**par)
#     cursor = conn.cursor()
#
#     try:
#         logging.info('fetch the count of rows from wk_export.ds_client_segmentation')
#         cursor.execute(sql_query)
#         count = str(cursor.fetchone()[0])
#         conn.commit()
#         cursor.close()
#         conn.close()
#         logging.info('the count of rows is fetched')
#     except (Exception, psycopg2.Error) as error:
#         cursor.close()
#         conn.close()
#         logging.info('Error: %s' % error)
#         raise AirflowException(f" Error: %s" % error)
#
#     send_data = {
#         "calc_ended": "X",
#         "calc_date": str(dt.date.today()),
#         "calc_rows": count,
#         "logical_date": local_tz.convert(context['logical_date']).to_date_string(),
#         "source_sys_cd": "DWH",
#         "code_flg": "l2_to_SAP_successful"
#     }
#
#     response = SRC_SAP.run(
#         json=send_data,
#         extra_options={'check_response': True}
#     )
#
#     logging.info(send_data)
#     logging.info(response)
#
#
# with DAG(dag_id='WF_MAIN_DATASETS_LOAD_L2_TO_L2',
#          description='WF_MAIN_DATASETS_LOAD_L2_TO_L2',
#          # schedule_interval='0 3 * * *',
#          schedule_interval=None,
#          catchup=False,
#          max_active_runs=20,
#          default_args=default_args) as dag:
#
#     get_load_id = PythonOperator(
#         task_id='get_load_id',
#         python_callable=md_dwh.get_date_for_session_dwh,
#         dag=dag)
#     workflow_registration = PythonOperator(
#         task_id='workflow_registration',
#         python_callable=p_workflow_registration,
#         dag=dag)
#     # create_dwh_flag = PythonOperator(
#     #     task_id='create_dwh_flag',
#     #     python_callable=p_create_dwh_flag,
#     #     dag=dag)
#     end_task = PythonOperator(
#         task_id='end',
#         python_callable=p_end,
#         dag=dag)
#
#     wait_for_l2_full_load = SqlSensor(
#         task_id='wait_for_l2_full_load',
#         conn_id='dwh',
#         sql="select * from md.dwh_flag where flag_cd = 'l1_to_l2_load_successfull' "
#             "and bussines_date = current_date - 1 ",
#         parameters={
#             'flag_name': 'загрузка данных из dwh l1 в dwh l2'
#         },
#         fail_on_empty=False,
#         poke_interval=60
#     )
#
#     sensor_success_end = ExternalTaskSensor(
#         task_id='wait_for_success_end',
#         external_dag_id='WF_MAIN_DATASETS_LOAD_L2_TO_L2',
#         external_task_id='end',
#         mode='poke',
#         poke_interval=100,
#         execution_delta=timedelta(days=1)
#     )
#
#     run_sys_kill_all_session_pg = TriggerDagRunOperator(
#         task_id='run_sys_kill_all_session_pg',
#         trigger_dag_id='sys_kill_all_session_pg',
#         reset_dag_run=True,
#         wait_for_completion=True,
#         execution_date='{{ dag_run.logical_date }}'
#     )
#
#     run_wf_data_preparation_for_reports = TriggerDagRunOperator(
#         task_id='run_wf_data_preparation_for_reports',
#         trigger_dag_id='wf_data_preparation_for_reports',
#         reset_dag_run=True,
#         wait_for_completion=True,
#         execution_date='{{ dag_run.logical_date }}', pool_slots=1, pool='dwh_l2'
#     )
#
#     email_failure = EmailOperator(
#         task_id='email_on_failure',
#         to=['b_alimov@ipakyulibank.uz'],
#         subject='Airflow DAG Execution Failure',
#         html_content=f'Your Airflow {dag.dag_id} encountered a failure.',
#         trigger_rule='one_failed',
#         dag=dag
#     )
#
#     with TaskGroup(group_id='segmentation_group') as segmentation_group:
#         load_ds_client_segmentation = TriggerDagRunOperator(
#             task_id='load_ds_client_segmentation',
#             trigger_dag_id='l1_to_l2_p_load_data_ds_client_segmentation_full',
#             reset_dag_run=True,
#             wait_for_completion=True,
#             execution_date='{{ dag_run.logical_date }}')
#         send_flg_to_sap = PythonOperator(
#             task_id='send_flg_to_sap',
#             python_callable=p_send_flg_to_sap,
#             dag=dag)
#
#         load_ds_client_segmentation >> send_flg_to_sap
#
#
#     wait_for_l2_full_load >> get_load_id >> workflow_registration >> sensor_success_end >> run_sys_kill_all_session_pg >> \
#        [run_wf_data_preparation_for_reports,segmentation_group] >> end_task >> email_failure