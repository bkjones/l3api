Common API Design Patterns
===========================
Typically, as a developer writing an API client, you go read the API documentation, which lets you know that 
"for this operation, you hit this specific url, using this method, and you use these params or payload". Then, 
you cut and paste a lot of the stuff that's in that documentation into your code. As a result, your code is very 
tightly coupled to the implementation choices the API developers made. The API developers documented their implementation, 
and asked you to abide by that, and you did. 

However, if the API developers need to:
 * change the url location of a resource because it's now a subresource of something else, 
 * change the method being used to perform an operation on a resource, 
 * change from using a dedicated endpoint for an operation on a resource to just allowing a POST on the resource itself to perform the operation, 
 * move from using GET with query params to using PUT with a payload for an operation, 
 
Then the developers will need to provide notice to the clients beforehand. Since any of these changes could require code 
changes on the client side, API teams might give anywhere from 2-6 months notice. This means that evolving the API is expensive 
for the team, happens slowly, and causes work for the customer of the API. 

Why The Web Works: Links and Forms
====================================

Designing an API in this way is common, but it ignores very important aspects of why the web became the platform it did in the first place: 
humans can navigate the web, and all of the sites on the web, without any prior knowledge about the design of the website, 
the operations available, the resources exposed, etc. 

Why is that possible? 

First, links are important. On the web, links are everywhere. Often, links on the web use an anchor tag on a word or phrase 
that describes what the link will do. This makes navigation fairly intuitive. 

Second, forms are also important. It allows users to provide input that enable operations like shipping, purchasing, logging in, 
adding comments, associating descriptions with images, etc. Forms work because, in general, the form is labeled according to 
its intent (the operation performed by hitting 'submit' on the form), and the fields the user needs to fill in are also labeled 
to indicate to the user what to do, and if fields are required or optional. 

So, you can pretty much get anywhere and do anything on the web, because there are links you can follow, which are labeled 
in some was as to where they'll take you, and there are forms that enable user input, and the forms & fields are also labeled 
to make it clear to the user what to do. 

Modern API Evolution
=====================
As it turns out, it's generally pretty easy for computers to do this web navigation using links and forms too. However, 
APIs aren't usually designed to let that happen.

Why? 

The cynical answer, which is the best I can muster today, is "Because people who didn't fully implement REST principles 
got on conference stages and told everyone that REST consists of resources that are always nouns, always human-readable, 
and verbs are always HTTP methods, and this is what CRUD stands for, and have a nice day." 

To be honest, it was an improvement over where we had previously been, so we took it. But most of the improvement was in 
terms of human readability and doing away with having to know about things like SOAP or WSDL. It was, at its best, 
Level 2 REST on the Richardson Maturity Model. We have APIs that are easy for humans to understand, but are not easy 
for computers to navigate without a lot of constant human intervention. 

What tier this architecture lives in according to some abstract model is not really the bit that's relevant to API developers and
their customers, though. What's relevant is the overhead introduced by *not* leveraging hypermedia for all it's worth. API 
developers and their clients (or, at least, the vast majority of them) aren't well-connected. A client developer probably 
helps build or maintain clients for internal and external services that number in the dozens. Likewise, an API developer could 
be supporting thousands of clients. To each, the other is faceless and 'in the noise'. 

API developers send email notifications that are often never seen. Client developers can completely fail to recognize the 
domain name on an email from an API provider, or funnel that email away into a 'noise' folder. This often results in changes 
taking place that are well-planned by the provider, but that nevertheless break the tightly-coupled client implementations.

In a panic, the client developer consults the API documentation. They look at the provider's dev blog. They might even just 
call your customer support line, who is probably staffed with folks who are going to tell them to look at the API docs, 
because they're not equipped to answer technical questions about the client's implementation. 

This is a poor experience. Architecture isn't responsible for all of it, but getting the approach toward API design right, 
and focusing on the right things, from the beginning, can help insure that this kind of thing is at least more of a rarity. 

What To Focus On When Approaching a Design
===========================================

In a perfect world, the API is treated like any other aspect of your company's product. The developers you serve are 
represented by an appropriate persona. Their use cases are well-known. There's a backlog in the issue tracker of feature 
requests. Some customers have been interviewed. There is data and metrics about the current use of the API endpoints, and 
it supports the prioritization of the backlogged requests. 

In a perfect world, there are success criteria associated with the design. Goals are set around adoption rate, feature 
penetration, response times & error rates, not to mention delivery dates being met so that the Marketing department can 
coordinate and get behind the release. 

This is all great, but this is all about implementation and post-release metrics - not the design approach. I've never seen an API team measure 
"Frequency of Disruptive Change", which would be the number of times per year (or maybe month) that the API provider makes 
a change to the API that forces client code changes. If target thresholds were set around this before implementation, it 
might force deeper thinking about the design to happen earlier. 

As developers and architects, it's not unusual to hear discussions about issues with our existing stack that are impacting 
what we are now trying to deliver. "Tight coupling" is a frequent term of disdain. But when we don't own the fallout from 
tight coupling, we frequently take the low road here ourselves. In designing an API to be used by nameless, faceless client 
developers, we take on the mindset of a bomber pilot, who never sees the destruction they cause their intended targets. 

A focus on decoupling the API from the client implementation should be a focus at the very outset. The approach and design 
discussions should center around, and be sensitive to, what each change or design element means in terms of "Frequency of
Disruptive Change". 

Why Level 3 REST Matters
============================

An API being a Level 3 design, as previously mentioned, doesn't much matter. However, it's a convenient handle to represent 
what's implied by a Level 3 REST API, and how those things benefit the team and the client. To my mind, utilizing hypermedia 
to enable clients to perform generic operations in their implementations instead of pasting hyper-specific URLs, methods, and 
data payloads, leaving them tightly chained to each individual piece of the APIs current implementation. 

In other words, customers are consuming the implementation of the API. They're not leveraging the design of the API. As such, 
maintenance overhead and disruptive change are more common.

One Approach at a Level 3 API, Illustrated
===============================================

This code repository illustrates some of the ideas that head toward a more mature Level 3 design. There's an API and a client 
which talks to the API. Clone it and check it out! 

The API itself is mostly cut-n-paste from the FlaskRestful project's example API. If you check out the client.py module, 
you'll notice that the only hard-coded URL is the one to the base '/' endpoint. The other hard-coded client-side elements are:

 * the names of the top-level resources ("todos")
 * the names of operations that can be performed on a resource
 * the field names in templated data payloads
 
With these things being true, it means that, from a design standpoint, you're committing heavily to those things being
hard-coded: changes to those things will require updates to the client code. Normal notification times & policies regarding 
developer relations & communication apply. 

However, this is still a much better position to be in, because if clients implement generic operations and don't hard-code 
anything else, API providers should be able to make pretty broad changes to the URI structure, the methods used for operations, 
and certain aspects of data payloads in a way that is transparent to the user. 

You should be able to use this repo to illustrate that. For example, I was able to change the 'complete-todo' operation from 
being a 'PUT' to the '/status' endpoint to being a 'POST' on the higher-level '/todos/{todo_id}' endpoint without making 
any changes to the client. 

In addition, there are some operations for which the server is in a position to know the fields *and* values required to 
be in the payload. In those cases, if changes in the API design require that data to change, but remain in the realm of 
data values the server knows, know changes will be required on the client end. Likewise, if a field that previously required 
substitution by the client changes & becomes 'fixed data' that the API can deliver, this should also not involve a code change 
on the client side. 

The Cost
==========

The design represented in this repository does have a couple of drawbacks. Namely: 

 * in the response to every request made by the client, they get a copy of all operations available on the resource & data required to perform them. 
 * the paradigm for client development is different, and requires a very solid documentation/education effort. Not many, if any, APIs like this exist. 
 
 For the first problem, the issue might be performance, and it might be an issue because of device platform, geographical location, 
 etc. Extra data just might not be desirable. It might be possible to enable a header that opts out of receiving parts of the data. 
 
 For the second problem, there are a couple of possible paths forward. One is to just create the client libraries and publish them. 
 The issue with this tends to be that developers make the creation of a client library in their favorite language their top
 feature request, and taking on the ongoing maintenance of the client libraries can become a real distraction to the API 
 development team. It might be better to take a second approach, which is to provide a wealth of documentation and code 
 samples, video explanations & walkthroughs, and do a thorough education campaign around the use of the API, illustrating 
 the benefits of such a design, and how to best leverage the design. 
 
 Looking Forward
 =================
 
 I think it's possible to improve on this design to further decouple the cient and the API implementation. This was only 
 a short foray into this way of designing an API, and I found one or two ways to further decoupling along the way, so I'm sure 
 there are more I haven't considered or thought of yet. 

 