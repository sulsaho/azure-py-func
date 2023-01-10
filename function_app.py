import azure.functions as func
import logging
import datetime
import sample_flask.app
import sample_fast.main

app = func.FunctionApp()
# app = func.WsgiFunctionApp(
#     app=sample_flask.app.app.wsgi_app, http_auth_level=func.AuthLevel.ANONYMOUS)
# app = func.AsgiFunctionApp(
#     app=sample_fast.main.app, http_auth_level=func.AuthLevel.ANONYMOUS)

# Learn more at aka.ms/pythonprogrammingmodel

# Get started by running the following code to create a function using a HTTP trigger.


@app.function_name(name="HttpTrigger1")
@app.route(route="hello", auth_level=func.AuthLevel.ANONYMOUS)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )


@app.function_name(name="mytimer")
@app.schedule(schedule="0 */5 * * * *", arg_name="mytimer", run_on_startup=True,
              use_monitor=False)
def test_function(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)


@app.function_name(name="QueueTrigger1")
@app.queue_trigger(arg_name="msg", queue_name="python-queue-items",
                   connection="AzureWebJobsStorage")
def test_function(msg: func.QueueMessage):
    logging.info('Python EventHub trigger processed an event: %s',
                 msg.get_body().decode('utf-8'))
