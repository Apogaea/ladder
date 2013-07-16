# What is Ladder

Ladder is an open source platform for exchanging tickets written in the Django
Web Framework.

It attempts to provide a simple, yet effective system for helping match people
who have tickets with people need tickets, on a first-come first-serve
basis.  The system attempts to leverage the idea that most burners would like
to know about the recipient of their ticket but allowing users to manually
select a recipient for their ticket based on a personal message provided by the
ticket requester.

# How it works.

## 1. Registration

Registration involves entering a valid email address and a display name.  An
email verification link is sent to the user, which will activate their account
and allow them to set their password.

## 2. Phone Verification

Once a user has activated their account, they must then provide a valid US
phone number, which is verified by either a code sent by SMS, or via a phone
call.  (See Twilio under the **requirements**).

The phone verification step is meant to loosely enforce one account per person.
While this is trivial for a motivated individual to bypass, it should help
restrict abuse.

## 3. Offerind and Requesting Tickets

Once a user has verified a phone number they may then either offer or request a
ticket.  offering and requesting tickets are mutually exclusive (*a user may
either offer or request a ticket but not both*)

### Requesting Tickets

A user have one active ticket request at any time.  When creating a ticket
request, the user is asked to enter a brief section of text about themselves
(see manual ticket matching under ticket offers). When a ticket is found to
fulfill the request, the user is contacted to confirm they still want/need a
ticket.  If they fail to respond within 48 hours, their ticket request is
deactivated and the offered ticket can then be offered to another user.

### Offering Tickets

A user may offer as many tickets as they want.

When the user creates the ticket offer, they may choose to automatically be
matched with a ticket request, or to manually select that match.

- Automatic matches are made based on a first come first serve basis, so the
  oldest ticket requests will be fulfilled first.
- Manual matches are still done on a semi first come first serve basis.  The
  user offering the ticket is presented with a small selection of the ticket
  requests from the front of the line and allowed to select which person they
  would like to give their ticket to, based on the personal message attached to
  each ticket request.

## 4. Confirming the match

Once an offer and request have been paired, the requester is notified via sms
and/or email, and given 48 hours to confirm the match.

- If the requester confirms, both users will be given each others contact
  information, and both the request and the offer are marked as being
  fulfilled.
- If the requester cancels the match or fails to respond to the confirmation
  request, their ticket request is cancelled, and the ticket offer is released
  back onto the market.

# Requirements

This app relies heavily on Twilio to interact with users via SMS and phone
calls.
