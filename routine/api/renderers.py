# import json

# from rest_framework.renderers import JSONRenderer


# class RoutineJSONRenderer(JSONRenderer):
#     charset = "utf-8"

#     def render(self, data, media_type=None, renderer_context=None):
#         # 만약 view가 error를 던지면 그 내부 'data'는 errors에 담기게 됩니다.
#         errors = data.get("errors", None)

#         # data에 errors가 있는지 확인하고, 만약 errors가 있다면 data를 'data' key에
#         # 넣지 않고 그대로 반환합니다.
#         if errors is not None:
#             return super(RoutineJSONRenderer, self).render(data)

#         # 그리고 우린 data를 'user' 안에 담아 json 형태로 render 해줍니다.
#         return json.dumps(
#             {
#                 "data": {"routine_id": "111114399999999999421111111"},
#                 "message": {
#                     "msg": "You have successfully created the routine.",
#                     "status": "ROUTINE_CREATE_OK",
#                 },
#             }
#         )
