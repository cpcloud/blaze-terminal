define [
    'react'
    'react-bootstrap'
    'components/AvailableTables'
    'jquery'
    'components/Terminal',
], (React, ReactBootstrap, AvailableTables, $, Terminal) ->

    PageHeader = ReactBootstrap.PageHeader
    Panel = ReactBootstrap.Panel

    React.createClass
        render: ->
            <div className="container">
                <PageHeader>Blaze Terminal</PageHeader>
                <Terminal />
                <Panel header={<h3>Tables in <code>db</code></h3>}>
                    <AvailableTables url="/data/tables" />
                </Panel>
            </div>
