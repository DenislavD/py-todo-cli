""" this script provides a command-line interface TODO functionality.

Supported commands: 
add "task"			Add a new task
list				List all tasks (show ✅ for done)
done <id>			Mark task as completed
delete <id>			Remove a task
clear				Delete all tasks (ask for confirmation)
search "keyword"	Show tasks containing keyword
stats				Show number of done vs pending tasks

"""
import sys
from datetime import datetime
import json

tasks = []

# print(sys.argv[1]) # always a string
def main():
	match sys.argv[1]:
		case 'add':
			...
		case 'list':
			todo_list()
		case 'done':
			...
		case 'undone':
			...
		case 'delete':
			...
		case 'clear':
			...
		case 'search':
			...
		case 'stats':
			...
		case _:
			sys.exit('No matching argument found. Try "list".')

	# print(sys.argv[1].lower())

	# timestamp = datetime.now()

def todo_list():
		tasks = get_tasks()
		# print(json.dumps(tasks, indent=2))

		for item in tasks:
			print(item.values())
			# print(list(map(lambda i: i.center(30), item.values())))
			...

def get_tasks() -> []:
	# read file, first line are the headers
	with open('tasklist.txt', 'r', newline='') as file:
		for line in file:
			items = line.split(',')
			tasks.append({
				'id': items[0],
				'title': items[1],
				'created_at': items[2] if items[2] == 'created_at' else datetime.fromtimestamp(int(items[2])).strftime('%d-%b-%Y'),
				'done': '✅' if items[3].strip() == 'y' else '', # ⚠
			})
			# print(line, end='')
	return tasks


if __name__ == '__main__':
	main()
