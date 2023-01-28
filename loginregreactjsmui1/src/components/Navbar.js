import { AppBar, Box, Toolbar, Typography, Button } from '@mui/material';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import { setUserInfo, unsetUserInfo } from '../features/userSlice';
import { unSetUserToken } from '../features/authSlice';
import { getToken, removeToken, storeToken } from '../services/LocalStorageService';

const Navbar = () => {
  const { access_token } = getToken()
  const handleLogout = () => {
    dispatch(unSetUserToken({ access_token: null }))
    removeToken()
    navigate('/login')
  }
  const navigate = useNavigate()

  const dispatch = useDispatch()
  var navbarButton=[];
  
  if(access_token)
  {
    navbarButton[0]=<Button component={NavLink} to='/dashboard' style={({ isActive }) => { return { backgroundColor: isActive ? '#6d1b7b' : '' } }} sx={{ color: 'white', textTransform: 'none' }}>Dashboard</Button> 
    navbarButton[1]=<Button component={NavLink} to='/profile' style={({ isActive }) => { return { backgroundColor: isActive ? '#6d1b7b' : '' } }} sx={{ color: 'white', textTransform: 'none' }}>Profile</Button>
    navbarButton[2]=<Button component={NavLink} to='/userauthtoken' style={({ isActive }) => { return { backgroundColor: isActive ? '#6d1b7b' : '' } }} sx={{ color: 'white', textTransform: 'none' }}>Tokens</Button>
    navbarButton[3]=<Button variant='contained' color='warning' size='small' onClick={handleLogout} >Logout</Button>
  }
  else
  {
    navbarButton[0]=<Button component={NavLink} to='/login' style={({ isActive }) => { return { backgroundColor: isActive ? '#6d1b7b' : '' } }} sx={{ color: 'white', textTransform: 'none' }}>Login/Registration</Button>
  }
  return <>
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant='h5' component="div" sx={{ flexGrow: 1 }}>MetaTrader</Typography>

          <Button component={NavLink} to='/' style={({ isActive }) => { return { backgroundColor: isActive ? '#6d1b7b' : '' } }} sx={{ color: 'white', textTransform: 'none' }}>Home</Button>

          <Button component={NavLink} to='/contact' style={({ isActive }) => { return { backgroundColor: isActive ? '#6d1b7b' : '' } }} sx={{ color: 'white', textTransform: 'none' }}>Contact</Button>
          
          {navbarButton}
          
          
        </Toolbar>
      </AppBar>
    </Box>
  </>;
};

export default Navbar;
