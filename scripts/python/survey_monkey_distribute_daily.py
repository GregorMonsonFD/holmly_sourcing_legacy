import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

def survey_monkey_distribute_daily(**kwargs):
  api_key = kwargs['api_key']
  server = kwargs['server']

  try:
    client = MailchimpMarketing.Client()
    client.set_config({
      "api_key": api_key,
      "server": server
    })
    response = client.ping.get()
    print(response)
  except ApiClientError as error:
    print(error)

  x = client.campaigns.replicate('df4d22a9b2')['id']
  client.campaigns.send(x)