Task management tool for personal use (so far).

This modules queries ChatGPT, using a directory of text files, in which
I manage tasks, as context.

The goal is to schedule or rescehdule incomplete tasks, understanding the user's
aspirations and needs for work-life balance.

Example query that works decently: "Reschedule important tasks to this week."

---

ideally i want to give every quest in every arc a date. complex since some 
tasks are moveable, some are not. 
 
right now, returns sets of scheduled tasks based on the query (from user input).

should not rely on user input and instead just instantly sort every arc file?

also, probably won't ever trust this tool completely; would always need to
review output.

## How to interact with this module

Place path to directory containing tasks in `src/constants.py`.
Place openai API key inside `src/constants.py`.
Modify `meta_context.md` to describe how you want tasks to be viewed, sorted
and shown. 