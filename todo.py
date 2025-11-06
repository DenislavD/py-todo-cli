""" this script provides a command-line interface TODO List functionality.
author: DenislavD
"""
import os
import sys
from datetime import datetime
import fileinput

file_path = os.path.dirname(__file__) + '\\tasklist.txt'
tasks = []

# sys.argv is always a string
def main():
	if len(sys.argv) < 2: sys.exit('No matching argument found. Try "help".')
	opt_arg = sys.argv[2] if len(sys.argv) >= 3 else None

	match sys.argv[1].lower():
		case 'list':
			todo_list()
		case 'add':
			if not opt_arg: sys.exit('Please provide a task description.')
			add(opt_arg)
		case 'done':
			if not opt_arg: sys.exit('Please provide an id to mark as complete.')
			replace_in_file(opt_arg, 3, 'y', f'Task {opt_arg} marked as complete.')
		case 'undone':
			if not opt_arg: sys.exit('Please provide an id to mark as not complete.')
			replace_in_file(opt_arg, 3, 'n', f'Task {opt_arg} marked as not complete.')
		case 'delete':
			if not opt_arg: sys.exit('Please provide an id to delete.')
			replace_in_file(opt_arg, -1, '', f'Task {opt_arg} deleted!')
		case 'search':
			if not opt_arg: sys.exit('Please provide a search string.')
			todo_list(opt_arg.lower())
		case 'clear':
			if input('⚠ Are you sure you want to clear ALL tasks? Type "Y" to confirm: ') == 'Y':
				clear_all()
		case 'stats':
			stats()
		case 'help':
			print("""
				Supported commands: 
				add "task"			Add a new task
				list				List all tasks
				done <id>			Mark task as completed
				delete <id>			Remove a task
				clear				Delete all tasks (ask for confirmation)
				search "keyword"		Show tasks containing keyword
				stats				Show number of done vs pending tasks""")
		case _:
			sys.exit('No matching argument found. Try "help".')


# action functions
def add(descr):
	tasks = get_tasks()
	next_id = int(tasks[-1]['id'] if len(tasks) > 1 else 0) + 1 # str to int, finally back to str..

	with open(file_path, 'a') as file:
		file.write(','.join(list(map(str, [next_id, descr, int(datetime.now().timestamp()), 'n']))) + '\n')
	print('Task added.')

def todo_list(filter=''):
		tasks = get_tasks(filter)
		if not tasks or len(tasks) < 2: sys.exit('No tasks found.')
		for item in tasks:
			print(item['id'].center(5), item['done'].center(8), item['title'].ljust(60), item['created_at'].center(10))

def get_tasks(filter='') -> []:
	tasks = []
	# read file, first line are the headers
	with open(file_path, 'r', newline='') as file:
		for line in file:
			items = line.split(',')
			if not tasks: # header row
				tasks.append({
					'id': items[0].capitalize(),
					'title': ' ' + items[1].capitalize(),
					'created_at': ' ' + items[2].replace('_', ' ').capitalize(),
					'done': items[3].strip().capitalize(),
				})
			elif len(items) > 1 and items[1].lower().find(filter) != -1: # search function added here
				tasks.append({
					'id': items[0],
					'title': items[1],
					'created_at': datetime.fromtimestamp(int(items[2])).strftime('%d-%b-%Y %H:%M'),
					'done': '✅' if items[3].strip() == 'y' else '❌',
				})
	return tasks

def replace_in_file(id, index, new_value, msg):
	result = False
	# inplace=True redirects STDOUT to the file in question, debug with False
	with fileinput.input(file_path, inplace=True) as file:
		for line in file:
			items = line.split(',')
			if items[0] == id:
				if 0 <= index <= 3:
					items[index] = str(new_value)
					print(','.join(items))
				else:
					print('', end='') # delete line
				result = True # id found, action taken
			else:
				print(line, end='') # don't change the line

	print(msg if result else 'Id not found. Please check the task list again.')

def clear_all():
	with open(file_path, 'w') as file:
		# add headers only
		file.write('id,title,created_at,done\n')
	print('All tasks cleared. You will regret this!')

def stats():
	aggregated_list = [1 if t['done'] == '✅' else 0 for t in get_tasks()[1:]] # heheh
	print(f'Done: {aggregated_list.count(1)}, Pending: {aggregated_list.count(0)}')


if __name__ == '__main__':
	main()
