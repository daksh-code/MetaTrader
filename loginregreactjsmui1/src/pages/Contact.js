import { useState } from 'react';
import { TextField, Button, Grid,Typography,TextareaAutosize } from '@mui/material';

function Contact() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Name:', name);
    console.log('Email:', email);
    console.log('Message:', message);
  };

  return (
    <div className="App" style={{textAlign:"center"}}>
          
    
    <Typography variant="h5">Contact Us</Typography>
    <form>

      <TextField
        style={{ width: "200px", margin: "5px" }}
        type="text"
        label="Name"
        variant="outlined"
      />
      <br />
      <TextField
        style={{ width: "200px", margin: "5px" }}
        type="text"
        label="Email"
        variant="outlined"
      />
      <br />
      <TextareaAutosize
        required
        aria-label="minimum height"
        minRows={8}
        placeholder="Message"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        sx={{
          width: "100%",
          padding: "10px",
          borderRadius: "5px",
          border: "1px solid gray",
          marginBottom: "10px",
        }}
      />
      <br />
      <Button variant="contained" color="primary">
        save
      </Button>
    </form>
  </div>
  );
}

export default Contact;
