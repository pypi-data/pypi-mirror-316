import cx_Oracle
import loggerutility as logger
from datetime import datetime

class Obj_Followup_Act:

    sql_models = []

    def check_or_update_followup_act(self, followup_act, connection):

        required_keys = [
            'obj_name', 'line_no', 'action_id'
        ]
        missing_keys = [key for key in required_keys if key not in followup_act]
        logger.log(f"Missing required keys for obj_followup_act table: {', '.join(missing_keys)}")

        if missing_keys:
            raise KeyError(f"Missing required keys for obj_followup_act table: {', '.join(missing_keys)}")
        else:
            obj_name = followup_act.get('obj_name', '')
            id = followup_act.get('id', '')
            line_no = followup_act.get('line_no', '')
            action_id = followup_act.get('action_id', '')
            action_type = followup_act.get('action_type', '')
            action_info = followup_act.get('action_info', '')
            conditional_expression = followup_act.get('conditional_expression', '')
            conditional_input = followup_act.get('conditional_input', '')
            chg_date = datetime.now().strftime('%d-%m-%y')
            chg_user = followup_act.get('chg_user', '').strip() or 'System'
            chg_term = followup_act.get('chg_term', '').strip() or 'System'
            max_retry_count = followup_act.get('max_retry_count', '')

            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM obj_followup_act 
                WHERE OBJ_NAME = :obj_name 
                AND LINE_NO = :line_no 
                AND ACTION_ID = :action_id
            """, obj_name=obj_name, line_no=line_no, action_id=action_id)
            count = cursor.fetchone()[0]
            logger.log(f"Count ::: {count}")
            if count > 0:
                logger.log(f"Inside update")

                update_query = """
                    UPDATE obj_followup_act SET
                    ID = :id, ACTION_TYPE = :action_type, ACTION_INFO = :action_info,
                    CONDITIONAL_EXPRESSION = :conditional_expression, CONDITIONAL_INPUT = :conditional_input,
                    CHG_DATE = TO_DATE(:chg_date, 'DD-MM-YY'), CHG_USER = :chg_user, CHG_TERM = :chg_term,
                    MAX_RETRY_COUNT = :max_retry_count
                    WHERE OBJ_NAME = :obj_name 
                    AND LINE_NO = :line_no 
                    AND ACTION_ID = :action_id
                """

                cursor.execute(update_query, {
                    'obj_name': obj_name,
                    'id': id,
                    'line_no': line_no,
                    'action_id': action_id,
                    'action_type': action_type,
                    'action_info': action_info,
                    'conditional_expression': conditional_expression,
                    'conditional_input': conditional_input,
                    'chg_date': chg_date,
                    'chg_user': chg_user,
                    'chg_term': chg_term,
                    'max_retry_count': max_retry_count
                })

            else:
                logger.log(f"Inside Insert")

                insert_query = """
                    INSERT INTO obj_followup_act (
                    OBJ_NAME, ID, LINE_NO, ACTION_ID, ACTION_TYPE, ACTION_INFO,
                    CONDITIONAL_EXPRESSION, CONDITIONAL_INPUT, CHG_DATE, CHG_USER,
                    CHG_TERM, MAX_RETRY_COUNT
                    ) VALUES (
                    :obj_name, :id, :line_no, :action_id, :action_type, :action_info,
                    :conditional_expression, :conditional_input, TO_DATE(:chg_date, 'DD-MM-YY'), :chg_user,
                    :chg_term, :max_retry_count
                )
                """

                cursor.execute(insert_query, {
                    'obj_name': obj_name,
                    'id': id,
                    'line_no': line_no,
                    'action_id': action_id,
                    'action_type': action_type,
                    'action_info': action_info,
                    'conditional_expression': conditional_expression,
                    'conditional_input': conditional_input,
                    'chg_date': chg_date,
                    'chg_user': chg_user,
                    'chg_term': chg_term,
                    'max_retry_count': max_retry_count
                })
            cursor.close()


    def process_data(self, conn):
        logger.log(f"Start of Obj_Followup_Act Class")

        # self.check_or_update_followup_act(followup_act, conn)
        logger.log(f"End of Obj_Followup_Act Class")
