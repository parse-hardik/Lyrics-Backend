const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
var app = express();
app.use(cors({ origin: true, credentials: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


app.post("/getQuery",(req,res)=>{
    var {query} = req.body;
    const {PythonShell} =require('python-shell');
    console.log('query is ', query);
    let options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    args: [query,0]
    };
    
    PythonShell.run('Processing.py', options, (err, results) =>{
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
        const arr=[];
        for(var i=0;i<10;i++){
            arr[i]=parseInt(results[i]);
        }
        res.status(200).json({result:arr,sge:"hello"});
    })
    
});

app.get('/', (req, res) => {
    res.status(200).json('Server is up and running')
    console.log('name is',window.ProcessedData.name)
})
process.env.PORT=5000;
app.listen(process.env.PORT || 5000, () => {
    console.log(`listening on port ${process.env.PORT}`);
    window.ProcessedData={
        name:"Hardik"
    }
    let options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    args: ['hello',1]
    };
    
    PythonShell.run('Processing.py', options, (err, results) =>{
        if(err)
            console.log(err)
        if(result)
            console.log('yes')            
    })
});