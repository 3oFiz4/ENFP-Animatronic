import datetime
from rich import print as log
import inspect
import discord
import json
import os
from dotenv import load_dotenv

with open("../config.json") as f:
    config = json.load(f)

# Get current time
def TimeCurrent():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def TimeToBirthdate(date):
    return datetime.datetime.strptime(date, "%d-%m").strftime("%d %B")

# Log if any commands related are triggered
def CogAlert(user_id=''):
    def isUIDExist():
        if user_id:
            return f'BY {str(user_id)}'
        else:
            return ''
    log(f'[green bold]COMMAND TRIGGERED {isUIDExist()}[/] [purple]{inspect.stack()[1][3]}[/] {TimeCurrent()}')

# Log if any io task related are triggered
def TaskAlert(func):
    log(f'[green bold]TASK TRIGGERED[/] [purple]{func.__name__}[/] {TimeCurrent()}')

# This is just our main embed. You can custom it though!
async def BaseEmbed(ctx, Title='', Desc='', Color=(config['EVERY_EMBED_COLOR']["COLOR_IN_RGB"]["R"], config['EVERY_EMBED_COLOR']["COLOR_IN_RGB"]["G"], config['EVERY_EMBED_COLOR']["COLOR_IN_RGB"]["B"]), field=None):
    """
    Sends a message to a Discord channel with a base embed. Or an embed that is have been ready.

    Parameters (! means important):
    !ctx (Context): You need to put this as the first parameter.
    Title (str, optional): The title of the embed. Defaults to an empty string.
    Desc (str, optional): The description of the embed. Defaults to an empty string.
    Color (tuple, optional): A tuple representing the RGB color of the embed. Defaults to a predefined color in the config.
    field (list of dict, optional): A list of fields to add to the embed. Each field is a dictionary with 'name', 'value', 'inline' keys. Defaults to None.

    Returns:
    discord.Message: The message that was sent.
    """
    embed = discord.Embed(
        title=Title,
        description=Desc,
        color=discord.Color.from_rgb(*Color)
    )
    if field is not None:
        for f in field:
            embed.add_field(name=f['name'], value=f['value'], inline=f['inline'])
    message = await ctx.send(embed=embed)
    return message

# Not finished yet. Do not use.
async def RaiseDBError(ctx, DBError):
    color = (255, 0, 0)
    error_message = str(DBError)
    if error_message == 'Database offline':
        solution = "The database appears to be offline. This could be due to network issues or the database server being down. Report this error to the Developer to check the network connection and the status of the database server."
        await BaseEmbed(ctx, "Database error", solution, color)
    elif error_message == 'Connection timeout':
        solution = "The connection to the database timed out. This could be due to network congestion or the database server being overloaded. Report this error to the Developer to check the network for any issues and consider increasing the timeout limit in the database configuration."
        await BaseEmbed(ctx, "Database error", solution, color)
    elif error_message == 'Invalid credentials':
        solution = "The credentials provided for the database are invalid. This means the username or password to access the database is incorrect. Report this error to the Developer to verify the credentials and try again."
        await BaseEmbed(ctx, "Database error", solution, color)
    elif error_message == 'Table not found':
        solution = "The table you're trying to access doesn't exist in the database. This could be due to a typo in the table name or the table not being created. Report this error to the Developer to check the table name and ensure it exists in the database."
        await BaseEmbed(ctx, "Database error", solution, color)
    elif error_message == 'Record not found':
        solution = "The record you're trying to access doesn't exist in the table. This could be due to a typo in the record ID or the record not being created. Report this error to the Developer to verify the record ID and ensure it exists in the table."
        await BaseEmbed(ctx, "Database error", solution, color)
    elif error_message == 'Query timeout':
        solution = "Your query took too long to execute. This could be due to the complexity of the query or the database server being overloaded. Report this error to the Developer to optimize the query and consider increasing the query timeout limit in the database configuration."
        await BaseEmbed(ctx, "Database error", solution, color)
    elif 'HTTP/1.1 404 Not Found' in error_message:
        solution = "The record you're trying to delete doesn't exist. Report to developer so we can verify the record ID and ensure it exists in the table."
        await BaseEmbed(ctx, "Database error", solution, color)
    else:
        solution = f"Unknown error: {DBError}"
        await BaseEmbed(ctx, "Database error", solution, color)
    # Add more error handling as needed :3

# Not finished yet. Do not use.
async def RaiseParamError(func, *args, **kwargs):
    sig = inspect.signature(func)
    params = sig.parameters
    missing_params = []
    for name, param in params.items():
        if param.default is param.empty and name not in kwargs and not args:
            missing_params.append((name, type(param)))
    if missing_params:
        missing_params_str = ' and '.join([f'`{name}` with a `{param_type}`' for name, param_type in missing_params])
        command_str = f">{func} {' '.join([f'[{name}]' for name, _ in missing_params])}"
        example_str = f">{func} {' '.join([f'{name}_example' for name, _ in missing_params])}"
        return f"Insufficient parameters. Your `{missing_params[0][0]}` parameter is `None`. Provide the {missing_params_str}\n**Command:**\n```\n{command_str}\n```\n\n**Example:**\n```\n{example_str}\n```"
    return None
