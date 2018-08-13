from django.shortcuts import render
from django.http import HttpResponse
import difflib
import datetime
import csv
from django.http import HttpResponseRedirect
from django.http import FileResponse
from .forms import FileForm
from .forms import UploadFileForm

# def handle_uploaded_file(file1,file2): # handle_uploaded_file is a function that takes 2 files uploaded by the users
# 	fileone = file1.readlines() # read lines from 1st file
# 	filetwo = file2.readlines() # read lines from 2nd file
# 	fileone =[line.decode("utf-8").strip() for line in fileone]
# 	filetwo =[line.decode("utf-8").strip() for line in filetwo]
# 	with open('results.csv', 'w') as outFile: # python creates a file called with difference.csv and start writing the differences
# 		for line in filetwo: # python compares the lines from both files
# 			if line not in fileone: # if line is not same
# 				print(line) # python writes those differences in difference.csv
# 				outFile.write(line+"\n") # every line python writes, adds a new row

def handle_uploaded_file(file1,file2): # handle_uploaded_file is a function that takes 2 files uploaded by the users
    fileone = file1.readlines() # define fileone and read lines from 1st file
    filetwo = file2.readlines() # define filetwo and read lines from 2nd file
    fileone =[line.decode("utf-8").strip() for line in fileone]
    filetwo =[line.decode("utf-8").strip() for line in filetwo]
    header = fileone[0].strip().split(',')
    # print(header)
    csv_old = [x.strip().split(',') for x in fileone[1:]]
    # print(csv_old)
    old_keys = [x[0] for x in csv_old]
    old_rows = {}
    for row in csv_old:
        key = row[0]
        if key in old_rows:
            old_rows[key].append(row)
        else:
            old_rows[key] = [row]

    csv_new = [x.strip().split(',') for x in filetwo[1:]]
    new_rows = []
    unchanged_rows = []
    changed_rows = []
    deleted_rows = []
    new_keys = {}
    for row in csv_new:
        key = row[0]

        if key in new_keys:
            new_keys[key].append(row)
        else:
            new_keys[key] = [row]

        if key in old_keys:
            if row in old_rows[key]:
                unchanged_rows
            else:
                changed_rows.append(['Changed'] + row)
        else:
            new_rows.append(['Added'] + row)

    for row in csv_old:
        key = row[0]
        if key not in new_keys:
            deleted_rows.append(['Deleted'] + row)

    print(sorted(unchanged_rows + changed_rows + new_rows + deleted_rows, key=lambda x: x[1:]))
    with open('results.csv', 'w') as f_output:
        csv_output = csv.writer(f_output, delimiter=',', lineterminator='\r')
        csv_output.writerow(['History'] + header)
        csv_output.writerows(sorted(unchanged_rows + changed_rows + new_rows + deleted_rows, key=lambda x: x[1:]))

def index(request): # index is a function for the upload button
	if request.method == 'POST': # POST method inserts something to the server
		print(request.FILES)
		form = UploadFileForm(request.POST, request.FILES)
		print(form.errors)
		if form.is_valid():
			print("cool")
			handle_uploaded_file(request.FILES.get('file1'),request.FILES.get('file2'))
			return HttpResponseRedirect('results/')
	else:
		form = UploadFileForm()
	return render(request, 'hello.html', {'form': form})

def results(request): # results is a function that sends difference.csv back to the user once the file is ready
    file_path = (r'C:\Users\Public\Documents\PycharmProjects\filecomparison\results.csv') #  adding an absolute path in the server, pinpoints that exact file, very important, r is to produce raw string and handle unicodeescape error
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'text/csv' # the type of the file that will be send is .txt/.csv
    response['Content-Disposition'] = 'attachment; filename=results.csv' # produces an attachment file for users to download called with difference in .csv file
    return response
