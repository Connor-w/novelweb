# from celery.result import AsyncResult
# from .celery_task import app
#
# id1 = '876b8637-79bd-430f-97ea-91cefb700156'
# id2 = '7d170fe3-b4d6-4d3c-bac9-49c61ed97b3e'
# async = AsyncResult(id=id2, app=app)
#
# if async.successful():
#     result = async.get()
#     print(result)
# elif async.failed():
#     print('执行失败')
# elif async.status == 'PENDING':
#     print('任务等待中被执行')
# elif async.status == 'RETRY':
#     print('任务异常后正在重试')
# elif async.status == 'STARTED':
#     print('任务已经开始被执行')
