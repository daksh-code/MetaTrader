import * as React from "react";
import {  Box, Toolbar, Typography, Button,TextField } from '@mui/material';
import { AlignHorizontalCenter } from "@mui/icons-material";
const Profile=() =>{
  return (
        <div className="App" style={{textAlign:"center"}}>
          
    
          <Typography variant="h5">AmeriTrade Login Details</Typography>
          <form>
    
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="City"
              variant="outlined"
            />
            <br />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="State"
              variant="outlined"
            />
            <br />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="Ameritrade username"
              variant="outlined"
            />
            <br />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="Ameritrade password"
              variant="outlined"
            />
            <br />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="region"
              variant="outlined"
            />
            <br />
            <Button variant="contained" color="primary">
              save
            </Button>
          </form>
        </div>
      );
    }
    
export default Profile;