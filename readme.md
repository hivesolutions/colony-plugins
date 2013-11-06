# [Colony Framework](http://getcolony.com)
This project contains the base plugins that provide the rich functionality associated with the Colony Framework. Here you'll find everything from the HTTP server, to the Web MVC stack, the Build Automation infrastructure and everything else we call base.

The Colony Framework is an open source plugin framework specification. Implementations of the specification offer a runtime component model, that allows for plugins to be installed, started, stopped, updated and uninstalled without requiring the application container to be stopped. The specification relies heavily on the Inversion of control principle, in order to make it easier for application components to discover and interact with each other.

Colony aims to eliminate the complexity typically associated with the creation of modular applications, through a simplified unified model for component development. Practical applications can range from modular enterprise software to application mashing.

## Quick start

* Download [Colony](http://hivesolutions.dyndns.org/integration_public/LATEST_SUCCESS/resources/colony_1.0.0_all.zip).
* Unzip the file, which will create a colony directory.
* Download the [Colony Base Plugins](http://hivesolutions.dyndns.org/integration_public/LATEST_SUCCESS/resources/colony-base-plugins_1.0.0_all.zip).
* Unzip the file's contents into the colony directory.
* Go to colony/scripts/<platform>
* Run the command 'colony'
* Check out that the [Colony Web Server](http://localhost:8080/) is up and running.
* Go to [Colony Manager](http://localhost:8080/manager/plugins#plugins) and manage your plugins.

## Features

* Build Automation infrastructure.
* Entity Manager ORM.
* Distribution stack for "viral" distribution.
* APNS Client.
* DNS Client.
* HTTP Client.
* LDAP Client.
* mDNS Client.
* SMTP Client.
* i18n stack.
* JSON-RPC Client.
* XML-RPC Client.
* BitTorrent Service.
* DNS Service.
* HTTP Service.
* IRC Service.
* mDNS Service.
* POP Service.
* SMTP Service.
* Telnet Service.
* XMPP Service.
* Thread pool.
* Full-text search infrastructure.
* MVC Stack.
* and more...

## Contributing

Although Colony is still in an early stage we're welcoming help for all kinds of work.
The best ways to get involved:

1. Join the [mailing list](http://groups.google.com/group/colony-users).
2. Send pull requests for bug fixes or new features and improvements.
3. Help make the [docs](http://getcolony.com/docs/colony/) better.

## Project information

* Colony Base Source: https://github.com/hivesolutions/colony
* Colony Base Plugins Source: https://github.com/hivesolutions/colony_plugins
* Web: http://getcolony.com
* Docs: http://getcolony.com/docs/colony/
* Mailing list: http://groups.google.com/group/colony-users
* Twitter: http://twitter.com/colonyframework

## License

Colony is an open-source project licensed under the [GNU General Public License Version 3](http://www.gnu.org/licenses/gpl.html).
