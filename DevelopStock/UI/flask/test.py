from flask import Flask,render_template
app =Flask(__name__)
@app.route('/')
def hello():
    # return 'hello world'
    class Person(objcet):
        name =u'黄勇'
        age =18
    p =Person()
    context ={
        'username':'知了课堂',
        'general':'男'
    }
    return render_template('aa.html',**context)
if __name__=='__main__':
    app.run()