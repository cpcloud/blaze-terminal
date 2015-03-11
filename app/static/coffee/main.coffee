require.config
    paths:
        react: '../libs/react/react.min'
        jquery: '../libs/jquery/dist/jquery'
        bootstrap: '../libs/bootstrap/dist/js/bootstrap.min'
        'react-bootstrap': '../libs/react-bootstrap/react-bootstrap.min'
        datatables: '../libs/datatables/media/js/jquery.dataTables.min'
        terminal: '../libs/jquery.terminal/js/jquery.terminal-0.8.8'
        filbert: '../libs/filbert/filbert'
        lodash: '../libs/lodash/lodash.min'

require [
    'react'
    'components/App'
], (React, App) ->
    React.render <App />, document.getElementById('app')
