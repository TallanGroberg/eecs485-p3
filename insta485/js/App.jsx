import React from 'react';
import PropTypes from 'prop-types';
import Header from './Header';
import Posts from './Posts';

const App = () => {
    return (
        <div>
            <Header />
            <Posts url="/api/v1/posts/" />
        </div>
    );
};

export default App;