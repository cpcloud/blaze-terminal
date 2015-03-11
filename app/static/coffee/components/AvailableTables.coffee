define [
    'react'
    'react-bootstrap'
    'jquery'
], (React, ReactBootstrap, $) ->

    Table = ReactBootstrap.Table

    React.createClass
        componentDidMount: ->
            callback = (data) =>
                @setState
                    tables: data
                    loading: false
                return

            $.get @props.url, callback, 'json'
            return

        getInitialState: ->
            tables: []
            loading: true

        getFullTable: ->
            body = @state.tables.map (row, i) ->
                rowData = row.dshape.pairs.map (pair, j) ->
                    data = pair.map (el, k) ->
                        <td key={k}><code>{el}</code></td>
                    <tr>{data}</tr>
                <tr key={i}>
                    <td key={i + 1}><code>{row.name}</code></td>
                    <td key={i + 2}>
                        <Table hover condensed>
                            <thead>
                                <th>Column</th>
                                <th>Type</th>
                            </thead>
                            <tbody>
                                {rowData}
                            </tbody>
                        </Table>
                    </td>
                </tr>
            <Table striped bordered condensed hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>dshape</th>
                    </tr>
                </thead>
                <tbody>
                    {body}
                </tbody>
            </Table>

        render: ->
            if not @state.loading
                @getFullTable()
            else
                <div />
