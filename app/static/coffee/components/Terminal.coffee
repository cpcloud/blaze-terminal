define [
    'react'
    'jquery'
    'terminal'
], (React, $) ->

    React.createClass
        componentDidMount: ->
            blaze = ->
                @push(((command, term) ->
                         $.jrpc('/compute', 'blaze', [command],
                                (json) -> term.echo(json.output))
                         return),
                {
                    prompt: 'blaze> '
                })
                return
            if @isMounted()
                node = $(@getDOMNode())
                node.css("overflow: auto")
                node.terminal([{
                    blaze: blaze
                }], {
                        prompt: '> '
                        greetings: 'Welcome to the blaze Terminal, type blaze to begin'
                        height: 400
                    })
        render: ->
            <div />
