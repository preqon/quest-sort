Personal task management tool. So far, just for my own use. If you're interested
in developing this tool for general use, feel free to contact me! 

This modules queries ChatGPT, using a directory of text files, in which
I manage tasks, as context.

The goal is to schedule or rescehdule incomplete tasks, understanding the user's
aspirations and needs for work-life balance.

Example query that works decently: "Reschedule important tasks that have not 
been completed to this week." The dates returned still don't make the most
sense.

In my own files, I refer to tasks as "quests", which is where the name of this
tool comes from.

## Example output

```
Prompt: Reschedule important but incomplete tasks to this week.
Here are the important but incomplete tasks rescheduled to this week:

- [ ] finish clearing phone notes #shallow ⏳ 2024-05-07
- [ ] update how i track expenses and budgeting methods #shallow ⏳ 2024-05-08
- [ ] [[shopping]] #rejuvenate 🕑 every week on Saturday ⏳ 2024-05-11
- [ ] [[gtec spring school]] #shallow ⏳ 2024-05-07
- [ ] job interview at 11 am on zoom, see gmail #shallow ⏳ 2024-05-07
- [ ] finish chapter 11 in a wavelet tour of signal processing #deep ⏳ 2024-05-07

Would you like to adjust any of these tasks further?
Prompt:
```

## How to interact with this module

Place path to directory containing tasks in `src/constants.py`.
Place openai API key inside `src/constants.py`.

Example `src/constants.py`:

```py

openai_api_key = "1234"
tasks_directory_path = "/user/documents/tasks/" 
```

Modify `meta_context.md` to describe how you want tasks to be viewed, sorted
and shown. Note: I use the 
[Tasks plugin for Obsidian](https://publish.obsidian.md/tasks/Introduction)
to manage tasks in text files, and so I have written `meta_context.md` to 
teach ChatGPT how to view/show tasks in a compatible format.

Run `src/questsort.py` and give a query related to your tasks. This is user
input or a command line argument.

---

## dev notes

ideally i want to use chatgpt to give every task in every file a scheduled date. 
complex since some tasks
already have dates (and are moveable); some have dates but are not moveable;
some do not have dates.
 
right now, returns sets of scheduled tasks based on the query (from user input).

should not rely on user input and instead just instantly sort every arc file?

also, probably won't ever trust this tool completely; would always need to
review output.