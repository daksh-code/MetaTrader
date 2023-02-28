import { Grid } from "@mui/material";

const Home = () => {
  return <>
    <Grid container justifyContent='center'>
      <Grid item sm={10}>
        <h1>Shalom!!!!</h1>
        <hr />
        <p>Welcome to MetaTrader, the platform that allows you to replicate trades from master traders to your TD Ameritrade account automatically. By signing up for our paid subscription, you can enter your TD Ameritrade credentials and our system will automatically replicate your trades. No need to manually enter trades, we take care of it for you. Sign up now and start replicating your trades with ease.</p>
      </Grid>
    </Grid>
  </>;
};

export default Home;

