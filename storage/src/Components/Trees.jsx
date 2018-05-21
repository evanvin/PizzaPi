import React from 'react';
import { geolocated } from 'react-geolocated';
import { Card, Typography, CardContent, Button, Grid } from '@material-ui/core';

class Trees extends React.Component {
  render() {
    console.log(this.props);
    return (
      <Grid item lg={6}>
        <Card>
          <CardContent>
            <Typography color="secondary" variant="headline" component="h2">
              Tree Information
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    );
  }
}

export default geolocated({
  positionOptions: {
    enableHighAccuracy: false
  },
  userDecisionTimeout: 5000
})(Trees);
