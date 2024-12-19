# Discord Embeds Pagination
Python package to create pagination with embeds in discord.py bots.

# Documentation
Import:
```python
from pagination import Pagination
```

Example use:
```python
@bot.command()
async def test_pagination(ctx):
    embeds = [
        discord.Embed(title="A", description="Desc", color=0x00ff00),
        discord.Embed(title="B", description="Desc", color=0x00ff00)
    ]
    pagination = Pagination(ctx, embeds)
    await pagination.init_messsage()
```

![screenshot](images/test_pagination.PNG)