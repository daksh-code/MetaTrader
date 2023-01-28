import * as React from "react";
import { useState } from "react";
import {  Box, Toolbar, Typography, Button,TextField,Alert } from '@mui/material';
import { AlignHorizontalCenter } from "@mui/icons-material";
import { useParams } from 'react-router-dom';
import { useUserAuthTokensMutation } from "../services/userAuthApi";
import { useSelector } from "react-redux";

const UserAuthToken=() =>{
    const [server_error, setServerError] = useState({})
    const [server_msg, setServerMsg] = useState({})
    const [sendUserAuthTokens,{isLoading}]=useUserAuthTokensMutation()
    const { access_token } = useSelector(state => state.auth)

    const handleSubmit=async (e)=>{
        e.preventDefault();
        const data = new FormData(e.currentTarget);
        const actualData = {
        api_access_token:data.get('Access_Token'),
        api_refresh_token: data.get('Refresh_Token'),
        api_consumer_key: data.get('Consumer_Key'),
        api_account_number: data.get('Account_Number')
        }
        console.log(actualData)
        console.log(access_token)
        const res=await sendUserAuthTokens({actualData,access_token});
        if (res.error) {
            console.log(typeof (res.error.data.errors))
            console.log(res.error.data.errors,"uvuvuvuhvuhv")
            setServerMsg({})
            setServerError(res.error.data.errors)
        }
        if (res.data) {
            console.log(typeof (res.data))
            console.log(res.data)
            setServerError({})
            setServerMsg(res.data)
        }
    }
  return (
        <div className="App" style={{textAlign:"center"}}>
          <Typography variant="h5">AmeriTrade Tokens Details</Typography>
          <Box component='form' noValidate sx={{ mt: 1 }} id='auth-token-form' onSubmit={handleSubmit}>
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="Refresh Token"
              variant="outlined"
              name="Refresh_Token"
            />
            <br />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="Access Token"
              variant="outlined"
              name="Access_Token"
            />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="Consumer Key"
              variant="outlined"
              name="Consumer_Key"
            />
            <TextField
              style={{ width: "200px", margin: "5px" }}
              type="text"
              label="Account Number"
              variant="outlined"
              name="Account_Number"
            />
            <Button type ="submit" variant="contained" color="primary">
              save
            </Button>
          </Box>
          {server_error.non_field_errors ? <Alert severity='error'>{server_error.non_field_errors[0]}</Alert> : ''}
          {server_msg.msg ? <Alert severity='success'>{server_msg.msg}</Alert> : ''}
        </div>
      );
};
    
export default UserAuthToken;