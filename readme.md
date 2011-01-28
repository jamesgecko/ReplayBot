ReplayBot
=========

Description
-----------
ReplayBot's purpose is to replay messages sent via REST to a groupchat channel.
It may be used like so:

    http://localhost:8880 -d This is a test message

You will need to set the login information in the script itself.

Dependencies
------------
Twisted. Twisted Words, Web, and Internet.

Conversation
------------
Here's the required Jabber conversation

Lifted from http://xmpp.org/extensions/xep-0045.html

    **Entering the room ->**
    <presence
        from='robot@ais/twisted'
        to='support@chat.ais/PaulRevere'> *<--- We are required to append our nickname to the end of the channel*
      <x xmlns='http://jabber.org/protocol/muc'>
        <history maxchars='0'/> *<--- Tell server not to send a history message*
      </x>
    </presence>

    **Recieving info about occupants <-**
    <presence
        from='support@chat.ais'
        to='james@ais/empathy'>
      <x xmlns='http://jabber.org/protocol/muc#user'>
        <item affiliation='owner' role='moderator'/>
      </x>
    </presence>

    <presence
        from='darkcave@chat.shakespeare.lit/secondwitch'
        to='russ@chat.ais/spark'>
      <x xmlns='http://jabber.org/protocol/muc#user'>
        <item affiliation='admin' role='moderator'/>
      </x>
    </presence>

    **Recieving presence of self <-**
    <presence
        from='support@chat.ais'
        to='robot@ais/twisted'>
      <x xmlns='http://jabber.org/protocol/muc#user'>
        <item affiliation='member' role='participant'/>
        <status code='100'/> *<--- You are not anon (might also be a seprate message)*
        <status code='110'/> *<--- This is you*
        <status code='170'/> *<--- The room is -bugged-, logged*
        <status code='210'/> *<--- we changed your nickname lol*
      </x>
    </presence>

At this point, we're good. Idle in the channel until we need to say something.

    **Sending message ->**
    <message
        from='robot@chat.ais/twisted'
        to='support@chat.ais'
        type='groupchat'>
      <body>The British are coming! The British are coming!</body>
    </message>

    **Recieving reflection of message <- (Confirmation, I guess?)**
    <message
        from='support@chat.ais/PaulRevere'
        to='robot@chat.ais/twisted'
        type='groupchat'>
      <body>The British are coming! The British are coming!</body>
    </message>

    #Ignore everything else. Or output it as debug info or something.



