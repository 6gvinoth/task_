from flask import Flask
from flask import render_template,request,redirect,flash,send_file
from tas import app

import ED as enc_dec
app.config['SECRET_KEY'] = '123456'
import hashlib ,json


def fun(id,name,dob,email,ph):
	
	#file=open("/home/vinoth/Desktop/task/block_genesis_hash.txt","r")
	file=open("/var/www/tas/block_genesis_hash.txt","r")

	block_genesis_hash=file.read()
	block_genesis_hash=eval(block_genesis_hash+']')
	file.close()

	block_genesis = {'prev_hash':block_genesis_hash[-1] ,'transactions': [id,name,dob,email,ph]}
	block_genesis_serialized_ = json.dumps(block_genesis, sort_keys=True).encode('utf-8')
	
	block_genesis_hash_ = hashlib.sha256(block_genesis_serialized_).hexdigest()
	block_genesis_serialized_=json.loads(block_genesis_serialized_.decode('utf-8'))

	#file=open("/home/vinoth/Desktop/task/block_genesis_hash.txt","a")
	file=open("/var/www/tas/block_genesis_hash.txt","a")
	file.write('"%s",'%block_genesis_hash_)
	file.close()
	#file=open("/home/vinoth/Desktop/task/block_genesis_serialized.txt","a")
	file=open("/var/www/tas/block_genesis_serialized.txt","a")
	file.write("'"+str(id)+"'"+':'+str(block_genesis_serialized_)+',')
	file.close()

	#file=open("/home/vinoth/Desktop/task/hash.txt","a")
	file=open("/var/www/tas/hash.txt","a")
	file.write("'"+str(id)+"'"+':"%s",'%block_genesis_hash_)
	file.close()
	
	#count+=1





@app.route('/')
def data():
    #file=open("/home/vinoth/Desktop/task/simple_db_data.txt","r")
    file=open("/var/www/tas/simple_db_data.txt","r")
    simple_db_data=file.read()
    simple_db_data=eval(simple_db_data+'}')
    file.close()

    #file=open("/home/vinoth/Desktop/task/hash.txt","r")
    file=open("var/www/tas/hash.txt","r")
    hash_=file.read()
    hash_=eval(hash_+'}')
    file.close()

    #file=open("/home/vinoth/Desktop/task/block_genesis_serialized.txt","r")
    file=open("/var/www/tas/block_genesis_serialized.txt","r")
    block_genesis_serialized=file.read()
    block_genesis_serialized=eval(block_genesis_serialized+'}')
    file.close()

    simple_db_data=enc_dec.decrypt_all(simple_db_data)
    data=simple_db_data
    return render_template("index.html",data=data,h=hash_,r=block_genesis_serialized)   

@app.route('/create')
def create():
    return render_template("create.html")


@app.route('/create_form',methods=['POST'])
def create_form():
    id=request.form['id']
    name=enc_dec.encrypt_3des(request.form['name'])
    dob=enc_dec.encrypt_3des(request.form['dob'])
    email=enc_dec.encrypt_3des(request.form['email'])
    ph=enc_dec.encrypt_3des(request.form["ph"])
    
    file_ = request.files['file']
    #file_.save("/home/vinoth/Desktop/task/cv/"+str(id)+".pdf")
    #file=open("/home/vinoth/Desktop/task/simple_db_data.txt","a")
    file_.save("var/www/tas/cv/"+str(id)+".pdf")
    file=open("/var/www/tas/simple_db_data.txt","a")
    file.write("'"+str(id)+"'"+":"+str({"name":name,"dob":dob,"email":email,"ph":ph})+",")
    file.close()
    
    fun(id,name,dob,email,ph)
    flash('User added successfully!')

    return redirect("/")

@app.route('/file')
def downloadFile():
    name=request.values["name"]
    #file="/home/vinoth/Desktop/task/cv/"+name
    file="/var/www/tas/cv/"+name	
    return send_file(file, as_attachment=True)
    
    
    
@app.route('/test')
def vinoth():
	
	#file=open("/home/vinoth/Desktop/task/block_genesis_hash.txt","r")
	file=open("/var/www/tas/block_genesis_hash.txt","r")
	block_genesis_hash=file.read()
	block_genesis_hash=eval(block_genesis_hash+']')
	file.close()
	#result={"block_hashes_":block_genesis_hash,"blocks":block_genesis_serialized}
	
	
	return block_genesis_hash
	#return render_template('block_chain.html',data=result,lenth=len(result["block_hashes_"]))
    

if __name__=="__main__":
    app.run(debug=True)
