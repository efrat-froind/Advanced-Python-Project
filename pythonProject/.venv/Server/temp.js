
import express from 'express'
const router = express.Router();
import Producer from '../Modules/producerModule.js';

router.get('/getEventProducer/:email', async (req, res) => {
    if(typeof(req.params.email) != "string")
        return res.status(400).send('הנתונים שגויים!!')
    try{
        const p = await Producer.findOne({ email: req.params.email });
        if (!p) {
            return res.status(500).send({ message: 'This producer doesn\'t exist' });
        }
        console.log("producerEmail: " + p.email + " ,producerName: " + p.name);
        res.send(p);
    }
    catch(err){
        res.status(500).send(err);
    }
});

router.post('/postEventProducer', async (req, res)=>{
    if(typeof(req.body.name) != "string" || typeof(req.body.phone) != "string" || typeof(req.body.email) != "string" ||typeof(req.body.shortDescreption) != "string"){
        return res.status(400).send("הנתונים שגויים!!")
    }
    else{
        console.log("in postEventProducer")
        const eventProducer = await new Producer({
            name: req.body.name,
            email: req.body.email,
            phone: req.body.phone,
            shortDescreption: req.body.shortDescreption
        })
        eventProducer.save()
        console.log(eventProducer)
        res.send({ message: 'Data received successfully!' });}
})

router.put('/putEventProducer', async (req, res)=>{
    if(typeof(req.body.name) != "string" || typeof(req.body.phone) != "string" || typeof(req.body.email) != "string" ||typeof(req.body.shortDescreption) != "string"){
        return res.status(400).send('הנתונים שגויים!!')
    }
    try{
        const p = await Producer.findOne({ _id: req.body._id });
        if (!p) {
            return res.status(500).send({ message: 'This producer doesn\'t exist' });
        }
        await Producer.updateOne({_id:req.body._id}, req.body);
        res.send(p.name +" is update")
    }
    catch(error) {
        res.status(500).send(error);
    }
});

export default router;