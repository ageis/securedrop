Install SecureDrop
==================

Install Prerequisites
----------------------

SecureDrop has some dependencies that need to be loaded onto the admin tails
stick prior to the installation of the server.

To load these dependencies, from the base of the SecureDrop repo run the
following commands:

.. code:: sh

    ./securedrop-admin setup

The package installation will complete in approximately 10 minutes, depending
on network speed and computing power.

.. _configure_securedrop:

Configure the Installation
--------------------------

Make sure you have the following information and files before
continuing:

-  The *Application Server* IP address
-  The *Monitor Server* IP address
-  The SecureDrop Submission Key (from the *Transfer
   Device*)
-  The SecureDrop Submission Key fingerprint
-  The email address that will receive alerts from OSSEC
-  The GPG public key and fingerprint for the email address that will
   receive the alerts
-  Connection information for the SMTP relay that handles OSSEC alerts.
   For more information, see the :doc:`OSSEC Alerts
   Guide <ossec_alerts>`.
-  The first username of a journalist who will be using SecureDrop (you
   can add more later)
-  The username of the system administrator
-  (Optional) An image to replace the SecureDrop logo on the *Source
   Interface* and *Journalist Interface*

   -  Recommended size: ``500px x 450px``
   -  Recommended format: PNG

You will have to copy the following required files to
``install_files/ansible-base``:

-  SecureDrop Submission Key public key file
-  Admin GPG public key file (for encrypting OSSEC alerts)
-  (Optional) Custom header image file

The SecureDrop Submission Key should be located on your *Transfer
Device* from earlier. It will depend on the location where the USB stick
is mounted, but for example, if you are already at the root of the SecureDrop
repository, you can just run: ::

    cp /media/[USB folder]/SecureDrop.asc install_files/ansible-base

Or you may use the copy and paste capabilities of the file manager.
Repeat this step for the Admin GPG key and custom header image.

Run the configuration playbook and answer the prompts with values that
match your environment: ::

    ./securedrop-admin sdconfig

The script will automatically validate the answers you provided, and display
error messages if any problems were detected. The answers you provided will be
written to the file ``install_files/ansible-base/group_vars/all/site-specific``,
which you can edit manually to provide further customization.

For example, you can have custom notification text be displayed on the
source interface. The source interface with a custom notification message is
shown here (the custom notification appears after the bolded "Note:"):

|Custom notification|

This custom notification can be configured by providing the desired message in
``custom_notification_text`` in ``install_files/ansible-base/group_vars/all/site-specific``.
For example, this can be used to notify potential sources that an instance is for
testing purposes only.

You may also customize the text of the issuer name of TOTP codes, so that when
the QR code is scanned in it provides a convenient identifier to your authentication
application.

When you're done, save the file and quit the editor.

.. _Install SecureDrop Servers:

Install SecureDrop Servers
--------------------------

Now you are ready to install! This process will configure
the servers and install SecureDrop and all of its dependencies on
the remote servers. ::

    ./securedrop-admin install

You will be prompted to enter the sudo password for the *Application* and
*Monitor Servers* (which should be the same).

The install process will take some time, and it will return
the terminal to you when it is complete. If an error occurs while
running the install, please submit a detailed `GitHub
issue <https://github.com/freedomofpress/securedrop/issues/new>`__ or
send an email to securedrop@freedom.press.

Once the installation is complete, the addresses for each Tor Hidden
Service will be available in the following files under
``install_files/ansible-base``:

-  ``app-source-ths``: This is the .onion address of the Source
   Interface
-  ``app-journalist-aths``: This is the ``HidServAuth`` configuration line
   for the Journalist Interface. During a later step, this will be
   automatically added to your Tor configuration file in order to
   exclusively connect to the hidden service.
-  ``app-ssh-aths``: Same as above, for SSH access to the Application
   Server.
-  ``mon-ssh-aths``: Same as above, for SSH access to the Monitor
   Server.

The dynamic inventory file will automatically read the Onion URLs for SSH
from the ``app-ssh-aths`` and ``mon-ssh-aths`` files, and use them to connect
to the servers during subsequent playbook runs.

.. |Custom notification| image:: images/install/custom-notification.png
