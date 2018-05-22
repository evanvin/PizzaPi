import React from 'react';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Card,
  Typography,
  CardContent,
  Button,
  Grid
} from '@material-ui/core';
const {IP} = require('./ip');

class Recordings extends React.Component {
  state = {
    data: []
  };

  componentDidMount = async () => {
    fetch(`http://${IP}:8008/tracks`)
      .then(res => res.json())
      .then(
        result => {
          this.setState({
            data: result
          });
        },
        error => {
          this.setState({
            data: []
          });
        }
      );
  };

  render() {
    const { data } = this.state;
    let results = '';
    if (
      data === null ||
      data === 'error' ||
      data === '' ||
      data === 'undefined'
    ) {
      results = [];
    } else {
      results = data;
    }

    return (
      <Grid item lg={6}>
        <Card>
          <CardContent>
            <Typography color="secondary" variant="headline" component="h2">
              Music
            </Typography>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell />
                  <TableCell>Artist</TableCell>
                  <TableCell>Recording</TableCell>
                  <TableCell />
                </TableRow>
              </TableHead>
              <TableBody>
                {results.map((item, i) => (
                  <TableRow key={'TableRow_' + i}>
                    <TableCell>
                      <img
                        alt={item.recording}
                        height="50"
                        width="50"
                        src={item.cover}
                      />
                    </TableCell>
                    <TableCell>{item.artist}</TableCell>
                    <TableCell>{item.recording}</TableCell>
                    <TableCell>
                      <Button
                        href={`http://${IP}:8008/download?recording=${
                          item.recording
                        }`}
                      >
                        Download
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Grid>
    );
  }
}

export default Recordings;
