""" this script provides a command-line interface TODO functionality.

"""
import os
import sys
from datetime import datetime
import fileinput

file_path = os.path.dirname(__file__) + '\\tasklist.txt'
tasks = []

# print(sys.argv[1]) # always a string
def main():
	if len(sys.argv) < 2: sys.exit('No matching argument found. Try "help".')

	match sys.argv[1]:
		case 'add':
			...
		case 'list':
			todo_list()
		case 'done':
			if len(sys.argv) < 3:
				print('Please provide an id to mark as complete.')
			else:
				mark_done(sys.argv[2])
		case 'undone':
			if len(sys.argv) < 3:
				print('Please provide an id to mark as not complete.')
			else:
				mark_undone(sys.argv[2])
		case 'delete':
			if len(sys.argv) < 3:
				print('Please provide an id to delete.')
			else:
				delete(sys.argv[2])
		case 'clear':
			...
		case 'search':
			...
		case 'stats':
			...
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

	# print(sys.argv[1].lower())

	# timestamp = datetime.now()

def todo_list():
		tasks = get_tasks()
		# print(json.dumps(tasks, indent=2))
		if not tasks: print('No tasks found.')
		for item in tasks:
			# print( *(list(map(lambda i: i.center(30), item.values()))) )
			print(item['id'].center(5), item['done'].center(8), item['title'].ljust(60), item['created_at'].center(10))


def get_tasks() -> []:
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
			else:
				tasks.append({
					'id': items[0],
					'title': items[1],
					'created_at': datetime.fromtimestamp(int(items[2])).strftime('%d-%b-%Y'),
					'done': '✅' if items[3].strip() == 'y' else '❌', # ⚠
				})
	return tasks

# refactor those with message -> argument
def mark_done(id):
	if replace_in_file(file_path, id, 'y'):
		print(f'Task {id} marked as complete.')

def mark_undone(id):
	if replace_in_file(file_path, id, 'n'):
		print(f'Task {id} marked as not complete.')

def delete(id):
	if replace_in_file(file_path, id, '', -1):
		print(f'Task {id} deleted!')

def replace_in_file(fpath, id, new_value, index=3) -> bool:
	result = False

	# inplace=True redirects STDOUT to the file in question, debug with False
	with fileinput.input(fpath, inplace=True) as file:
		for line in file:
			items = line.split(',')
			if items[0] == id:
				if 0 <= index <= 3:
					items[index] = str(new_value)
					print(','.join(items))
				else:
					print('', end='')
				result = True # action taken
			else:
				print(line, end='')
	return result

if __name__ == '__main__':
	main()
