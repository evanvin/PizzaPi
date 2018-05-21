import React from 'react';
import { Grid } from '@material-ui/core';
import CssBaseline from '@material-ui/core/CssBaseline';

import Recordings from './Recordings';
import Trees from './Trees';

const containerStyle = {
  margin: '50px'
};

class Index extends React.Component {
  render() {
    return (
      <React.Fragment>
        <CssBaseline />
        <div style={containerStyle}>
          <Grid container spacing={16}>
            <Recordings />
            <Trees />
          </Grid>
        </div>
      </React.Fragment>
    );
  }
}

export default Index;
