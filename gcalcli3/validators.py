# set-color option validator
import click
import re


def validate_set_color(ctx, param, value):
    valid_options = ["owner", "writer", "reader",
                     "freebusy", "date", "nowmarker", "border"]
    for opt in value:
        if opt[0] not in valid_options:
            raise click.BadParameter(
                "type should be one of the following " + str(valid_options))
    return value


# reminder option validator
def validate_reminder(ctx, param, value):
    if value is False:
        return value
    for rem in value:
        match_obj = re.match("^(\d+)([wdhm]?)(?:\s+(popup|email|sms))?$", rem)
        if not match_obj:
            raise click.BadParameter(
                "Reminders should be in the form of 'TIME METH' or 'TIME'")
    return value