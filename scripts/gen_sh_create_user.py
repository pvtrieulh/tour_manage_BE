import pandas

df = pandas.read_csv('tk_aic.csv')
with open('..\..\scripts\gen_supereditor.sh', 'w') as output_file:
    str = 'source ~/app/production/venv/bin/activate\ncd ~/app/production/tetviet/src/tetviet/'
    output_file.write(str)
    output_file.write('\n')
    for i in range(df['User'].count()):
        per = df['vaitro'][i]
        per = per.split('/')[1].strip()
        if per == 'Admin':
            permission = 'createsupereditor'
            str = 'python manage.py '+permission+' --username '+df['User'][i]\
                  +' --password '+df['Pass'][i]+' --noinput --email '+df['Pass'][i]+'.com'
            output_file.write(str)
            output_file.write('\n')

with open('..\..\scripts\gen_editor.sh', 'w') as output_file:
    str = 'source ~/app/production/venv/bin/activate\ncd ~/app/production/tetviet/src/tetviet/'
    output_file.write(str)
    output_file.write('\n')
    for i in range(df['User'].count()):
        per = df['vaitro'][i]
        per = per.split('/')[1].strip()
        if per == 'Editor':
            permission = 'createsupereditor'
            str = 'python manage.py '+permission+' --username '+df['User'][i]\
                  +' --password '+df['Pass'][i]+' --noinput --email '+df['Pass'][i]+'.com'
            output_file.write(str)
            output_file.write('\n')

output_file.close()
print("Success create")
