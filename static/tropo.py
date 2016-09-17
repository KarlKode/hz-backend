import urllib
import urllib2


def debug(message):
    url = 'http://hz.wx.rs:5001/tropo/debug'

    values = {
        "message": message,
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()


def submit(status, needs, skills):
    url = 'http://hz.wx.rs:5001/tropo'

    values = {
        "status": status,
        "needs": needs,
        "skills": skills,
    }

    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print (the_page)


def my_ask(question, answers):
    while True:
        result = ask(question, {
            "voice": "Kate",
            "choices": answers,
            "mode": "speech",
            "attempts": 3,
        })

        wait(1000)
        result2 = ask("You answered " + result.value + ". Is this correct?", {
            "voice": "Kate",
            "choices": "yes, no, correct, incorrect",
            "mode": "speech",
            "attempts": 1,
        })
        if result2.value in ("yes", "correct"):
            return result.value


debug('start...')

wait(1000)
say("Welcome to the automated catastrophe system.")

wait(500)

status = my_ask("What's your status? Respond with ok, injured or heavily injured.", "ok, injured, heavily injured")
debug('status: ' + status)
wait(1000)

say("What's your address?")
wait(3000)

needs = my_ask("Do you need help? Respond with none, medical assistance, shelter, food, water.", "none, medical assistance, shelter, food, water")
debug('needs: ' + needs)
wait(1000)

skills = ''
if status == 'ok':
    skills = my_ask("Can you provide any help? Respond with none, medical assistance, food or water", "none, medical assistance, food, water")
    debug('skills: ' + skills)
wait(1000)

say("Thank you!")
submit(status, needs, skills)
wait(500)

debug('end')
