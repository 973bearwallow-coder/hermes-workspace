# Source: spark-2026-09-09

URL: https://fathom.video/share/MyX5zaTFBzFgbMJA-3zzfycWSKddFyqq

153 mins

Impromptu Google Meet Meeting

Sep 9, 2026

0:00

1

SummaryTranscriptAsk Fathom

Resume Auto-Scroll

Aaron (WeDigCode)

> Welcome to the 730 Spark, Builders. Coffee seeded the threads. Now we go deeper. Here is the flow. Screen shares welcome.

> We pick one live problem and stay with it. A few deeper cuts. Hybrid local, chat GPT desktop plus olama, or cursor pointed at local.

> A written merge rule for agent merge, origin versus github as source of truth, a clod code packing list, initial prompt, credential scrub, fail if the sandbox cannot start, one guild MCP rule from the OWASP top 10, same grok 4.6, three different context numbers depending on who bills you, multi-route agent sessions, fable watermarks on text after August 2nd, cursor computer use on a machine you host, jump in, react, disagree, show something on screen.

> Leftover heat returns to morning coffee hour. Never give up. Every hand you lift lifts your own. Let's build. to the 730 Spark Builders, coffee seeded the threads, now we go deeper, here is the flow.

Rick Rodriguez

> ScreenShares welcome, we pick one live problem and stay with it. A few deeper cuts, hybrid local, chat GPT desktop plus olama, or cursor pointed at localhost.

> A written merge rule for agent merge, origin versus GitHub as source of truth. A Claude code packing list, initial prompt, credential scrub, fail if the sandbox cannot start.

> One guild MCP rule from the OWASP top 10. Same grok 4.6, three different context numbers depending on who bills you.

> Multi-route agent sessions. Fable watermarks on text after August 2nd. Cursor computer use on a machine you host. Jump in, react, disagree, show something on screen.

> Leftover heat returns to morning coffee hour. Never give up. Every hand you lift lifts your own. Let's build. Good evening, everybody.

> Welcome to the Spark. Hey, Patrick. How are you doing, Rick?

Patrick Thomas

> Pretty good, pretty good. It's starting to get dark again early.

Rick Rodriguez

> Oh, no, is it? hate that. Did you get the time change again?

Patrick Thomas

> Oh, you didn't like that. Well, it's not the time change yet, but the sun is slowly starting to set earlier and earlier.

> I like it when it sets, like, at 830.

Rick Rodriguez

> Yeah, me too. I think it sits.

Patrick Thomas

> I've never seen a dog man. She does it because she thinks it gets. Yeah. So, today, I added something a little extra.

Rick Rodriguez

> I... Titled some of the notes in chat so that everybody knows what they are, and then also I created a link to the Discord Builders Lounge so that after our meets, our Google meets, if people wanted to stay on here, they can stay on here, but eventually what I'm going to do is I'm going to have things scrolling at the end of the meets, telling people that they can continue things over on the Discord server.

> That's going to serve a couple different purposes. First of all, it has a lot more options, a lot of bells and whistles as we talked about this morning.

> Let me close this door here. And also, it's a place where people can always pop in when there's no Google Meet, leave their questions, look at anything that we post in there.

> So I won't have to really rely on just the Google Meet times. They'll be able to get information and actually converse with other people.

> they do... ... ... And stuff at any time they like. All right.

Patrick Thomas

> Do you have anything to do with this disability? Where are you at again? Where are you at? New York.

> New York. that's dumb. Yeah, so from California. Every year, more than 600,000 people go missing in the States.

Rick Rodriguez

> So, also, I have, there was something in the notes that I haven't heard about before. And let me just bring them up here.

> That was the, what is this?

Patrick Thomas

> Does anybody know what this origin is?

Rick Rodriguez

> Is it a GitHub-like thing? Let me bring up the, throw the link in there. It's in the notes, in the Spark notes, but let me just throw out an extra link in there.

> Or It's in the SparkNotes, let me also pop that in the chat, not sure what that is, it's CursorsGit for storing and sharing code, great origin repositories, clone, push, pull, mirror, automation.

> And some cloud agents. Interesting. Another shiny object. Aaron, have you seen that before? The origin for Cursor? I haven't seen it yet.

> I can barely hear you, Aaron. My headphones are horrible on my phones today.

Aaron (WeDigCode)

> That's better. That's better. Yeah. But no, I haven't seen the Cursor origin yet. I just Googled in that, too.

> Interesting.

Rick Rodriguez

> Now that I'm just learning, I'm just learning GitHub and Discord. Now they throw this origin in there. Just stick with GitHub.

> That's more it's got more of a foothold. You know, have you ever heard radical ideas threaten institutions, which in turn become institutions which are then threatened by radical ideas?

> No. That was that was something I heard a long time ago, but it always it's one of those things that always stuck with me.

> It's very true. Who has something they would like to share? Oh, Patrick, were you saying that you were working on something that you were going to do something for tonight?

Patrick Thomas

> Yeah, I did a couple of things. I of things. I just did of things. couple of things in Brockbox.

> One of them was, and I put them in the air, Builderscape, and I was going put them in the nets too.

> Basically, when we were talking, you know, about the sandbox, you know, when Brockbox starts running slow, or if there's, oh, if there's a problem, one of the things is if you're, if you're using Brockbox, you're using the air, AI, it's using the virtual private computer, the VPS, if you have to reboot it, or if, if it doesn't upgrade and restarts anything that you've installed in there, you lose, because it's in a, it's in a sandbox environment.

> So, um, one of the things I did, there's two things I did today with that, and one of them is, I had it right, I had chat, right, the verbiage,

> So before I did, I said, come up with the verbiage, and I put this in the chat in the previous meeting.

> I'll have to go back and take a look at that, yeah.

Rick Rodriguez

> Yeah, it's in the AI Builders Guild.

Patrick Thomas

> I posted it. It's basically a disaster recovery for your VPS. So if you've got a bunch of stuff, like for instance, I have the Edge browser and some other stuff loaded in there.

> So it created a disaster. And it did it local. I guess it did some of it in Git, but some of it local.

> But basically, so if it gets messed up and has to be reboot for any reason, you just tell it to restore it.

> It restores your environment in a matter of, you know, whatever, a minutes. Okay, yeah, I see it right now.

> Just a couple hours. Yeah, that's an older one, but just scroll down. And the other thing I did was, after that was the, it's, I noticed the thing runs slow.

> So I had it right, it wrote a thing called, and it's a one word command called lag. If it's, if it's running slow, and I type lag, it does this whole routine, or skill that I had chat GPT write the verbiage for, and it goes in and, and, like, kills, like dead, or Google tabs, it does.

> It goes through it, and instead of rebooting the machine, it goes through it and cleans it all up. It kills processes and stuff?

> Yeah, a bunch of stuff, and it works, and I tested it, and it makes a big difference. Oh, interesting.

> So I put that in there, too. Instead of seeing what's running and seeing how much it's using and then killing each process by itself.

Rick Rodriguez

> Yeah, and I can post that up there, and the routine's just called lag.

Patrick Thomas

> So if I type lag, it runs that, and then the thing starts running way faster. Oh, that's perfect. Thank you.

> I'm going to have to check that out, yeah.

Rick Rodriguez

> Keith would really be able to use that. A lot of times, he gets really laggy, and he says he has to go in there and turn a lot of stuff off.

> So that's what I've been doing mostly, some other work-related stuff.

Patrick Thomas

> That's about it. Yeah.

Rick Rodriguez

> I think John was working on it.

Patrick Thomas

> I don't know if he got it finished, but he was working on a project he was all excited about.

> Before we dive into that really quick, can we go into the VPS a little bit deeper with the GrokBot cursor VPS?

Jobi Armstrong

> Because I asked GrokBot how I could utilize their VPS, and they're like, oh, it's locked. You can't get to it.

> So I know we've talked about this, but I think I just missed the plot at some point because I'd like to use it.

> Or are you just literally using it inside the cursor app? How are you?

Rick Rodriguez

> No, actually, and then I had a question for Patrick on another topic on that. So the VPS, I went and I installed Hermes in the VPS because you have a CLI in there, so you can actually install Hermes in the Grok VPS.

> But today I got a message saying, because I started doing some stuff in there to create, what was it?

> All right. perfect. gosh. I was doing something with Hermes in there, and I was creating the Discord bot, and I found out that it was in a sandbox, but then today I must have left some stuff running.

> I got a message that 75% of my OAuth had been used, and I'm like, but I haven't been doing anything, and like 75% of my OAuth, so I went in there and I just, I killed everything in my VPS, but yeah, you can install Hermes and everything, but I'm just, I've just touched the surface of it.

> Patrick's really, really putting it through the paces.

Patrick Thomas

> Yeah, and I think John's the one that had it right in routines, right to the VPS, you're talking about having, running it for the hardware, not using the AI side of it?

Jobi Armstrong

> Is that what you're talking about? How do I, how do I actually use the VPS to start running my projects?

Patrick Thomas

> Because I, like I said, I don't know what, are you using it through Grok Pot, through the Grok Pot interface?

Jobi Armstrong

> końca place? You're using it through Kroc.

Patrick Thomas

> Cloud Browser. Like, what are you doing? Yeah.

Jobi Armstrong

> I'm I'm using the front end.

Patrick Thomas

> I'm using the desktop interface of GrokBot, but I think John's using something else. Is he in the call? Yes, he is.

> Yeah, I asked it. Yeah, you can use the VPS for GrokBot, but you can't. He said if you want to, okay, if you want one machine that Cursor and other programs both use years, like I can't SSH into their VPS is what I'm trying to get at.

Jobi Armstrong

> I'm trying to, I thought you could use it like a VPS that you buy from hosting or whatever. It's got a terminal in it.

Patrick Thomas

> got a terminal in it. You should be able to SSH. Yeah, let me ask it. I said how do I utilize the Cursor slash GrokBot VPS?

Jobi Armstrong

> I have the Cursor subscription and want to take advantage of the VPS not only in Cursor but also in other programs.

> And it says the Cursor subscription isn't a personal VPS. You can start them from cursor slash agents, pod dropdown, yada, yada, but you don't get SSH, public IP, or a login that other programs can use, is what this is what Rockbot told me.

Rick Rodriguez

> I'm going to start mine up here, and let's see here, connecting. I'll ask, and I'll ask Rockbill as well.

Patrick Thomas

> Can you post that question? Can you throw it in the chat? Do I have to retype it? There you go.

> Thank you.

Rick Rodriguez

> I'm going to go ahead and share this real quick. I just touched a little, just lightly on this, but let me share it and see if I can share this, what I've done so far.

> So I installed Hermes, so I got the Hermes CLI in there, so you can do that. And then I started using Hermes to try and create the Discord back and forth with the Discord bot and have it run from here and then reach out and put the Discord bot that I created on Hermes for Nova and put that in Discord.

> But it landed in Discord, but it wasn't able to talk. So you could ask a question, but it would never answer you.

> So that's... Yeah, I'm asking, so basically you're saying how do I open up the SSH?

Patrick Thomas

> You're saying the SSH port would have to be open on the... Yeah.

Jobi Armstrong

> Like I get that you're using, I mean, I understand you're using the power of the GrokBot VPS, but the VPS doesn't seem to be like something that me and you, we could share an association to it together is what I guess I'm getting at.

> It doesn't seem like you have full control like you would if you were to buy or rent one from Hostinger.

> No, that's the challenge. It's limited.

John Mackenzie

> And with the VPS, you can't, like with Hostinger, you can actually set things like region. You can scale up and scale down and also allocate things like GPS to it, a GPU.

> You can't do any of that with the VPS. It's like a very basic black box. But if you find a use case for it that sits nicely in terms of your execution of it, it'll work well.

Rick Rodriguez

> So the art is now trying to run experiments to do that.

John Mackenzie

> I ran an experiment a few weeks ago, and I moved AI compute off to deterministic compute, and the equivalent power of the AI compute was worth, if I'd ran it for the whole year, I think it was worth a couple hundred thousand, sorry, the whole month, it was worth a couple hundred thousand dollars.

> But I ended up, I think I ran it for 10 days or 14 days like that, so it was probably worth over $100,000 of AI compute.

> Is that how you had $200,000 worth of, was that what that was referring to?

Jobi Armstrong

> Well, no, that was one part.

John Mackenzie

> On pure AI compute, on a year, on my current usage, I'm sitting up for about $226,000 of pure API commercial usage.

> But the other thing is, And I haven't factored at the moment, but I noticed today that Claude Code has got a 50% overage that it has given everyone since the 13th of May, and it's going to, at the moment, it's earmarked to complete on the 13th of September.

Patrick Thomas

> So, but they must have kept rolling it out and rolling it, because they're in a price war with OpenAI.

John Mackenzie

> And the other thing is, did anyone notice that their codex got reset again sometime in the last 24 hours, because I was sitting at a high use rate with three or four days to go, thinking I'll slow down weight on that particular account, and then it got reset again.

> It did extend. extend the week, I don't think.

Patrick Thomas

> But whatever it did is, it didn't extend the week, because I triggered...

John Mackenzie

> I triggered one of my reset coupons or codes 36 hours ago or something like this, so that time has disappeared, but I got on my compute back again, and I'd already used most of that compute, so I was sitting at about 85% use again, so when they did the reset, I got 85% of my use back again.

> I got two reset for myself.

Patrick Thomas

> No, no, no, they must have also done just a hard reset, right?

John Mackenzie

> Just in quadra, in quadra, GG.

Patrick Thomas

> Codex, yeah. I'm at 100% right now with two resets sitting there.

John Mackenzie

> And I don't know if you'd used any of that, but all I know is I capped out one, 100%, I hit a reset, got that to 85%, and that was in 36 hours.

> They did a, they just did a reset, not a code, they just did I've got 100% back again, and now I've been soaking that back up, and I've still got my other two resets on this computer.

> The other thing is I've got my other computer codex working on my other computer.

Patrick Thomas

> Now I'm just about to hook them together. So I've got two $25 codex accounts now that I'm starting to chain together.

John Mackenzie

> The codex is becoming a bigger part of my use case, and I'm doing a lot of testing in Grok at the moment, and I'm waiting on some of those tests to come back.

> I've moved over to heavy codex.

Patrick Thomas

> I actually had to repeat my subscription.

Jobi Armstrong

> I'm not the $200, but I'm on the $100 because the $20 plan just wasn't cut. It was eaten through asterisk tokens like crazy, but the $100 is manageable.

> But it's doing wonderful things.

Patrick Thomas

> I've been playing around with it quite a bit. I've been auditing.

Jobi Armstrong

> A lot of my projects are taking the code base and dropping it into Codex, Astra, Kai, and have a full audit, and then putting together like a 10 or 12-page PDF audit, and then I'll fork it with Codex and start building it in that direction, but I'll also drop that audit back into Claude and have Claude look at it, and it'll be like, yeah, this is good, and actually pointed out quite a few different things, but here's where I disagree with it as So it's interesting to jump back and forth between LLMs and see the difference in opinion when you do stuff like that.

> So I've been doing that with a few of my projects. I will say that I like the design. So on the UI side, the design aspect, and I did this before, think, when I was, Claude is really good with documents, creating spreadsheets, but ChatGPT was always better at putting together like a picture or like some.

> So I'm putting together design boards with Codex right now and then, so the two projects I'm revamping right now is my permit portal project and then the contractor compliance program, which I've been doing a lot.

> And that's what I've been utilizing the DROC or the Cursor cloud agents. I've been using Fable 5.1 inside of Cursor because it's a different usage.

> It's obviously it's their subscription. So I've been searching all the country's jurisdictions and putting them into a database. Oh, yeah, yeah, yeah, that's going to be huge if you can, if you can not that.

> Yeah.

John Mackenzie

> I'll show you. So got an answer for you, and I, because it was long, so I had Dr.

Patrick Thomas

> Will put it out on my web server. Thanks.

Jobi Armstrong

> You click on that. It'll tell you how to do it and use tail scales.

Patrick Thomas

> Bye. That's what I already have anyway.

Jobi Armstrong

> But I think it gives you the machine name.

Patrick Thomas

> have to tell it box, your tailscaling in the box. It gives you the instructions on how to do it on your PC.

> Yes, you should be able to do tailscalesshbox.grop.box. You should be able to do it. The instructions are out there.

> I appreciate that. I just clicked on it. I'm going to save them and set that up tonight.

Jobi Armstrong

> That's awesome. Using tailscalesshbox noticing, like, if you want to do a group project, you can create a server and have a group project, and everybody can change your tailscalesshbox a really valuable tool, if anybody is in, like, group projects at all.

> Yeah, I mean, that would be great.

Patrick Thomas

> I haven't done group projects, but I'm down to try it. Oh, I sent some documents to Yasmin. I will put them in here as well for everybody to use.

> I just got to find them really quick.

Jobi Armstrong

> Cool.

Rick Rodriguez

> I could probably, I probably could have threw them out up into like, uh, the notebook L.M.

Patrick Thomas

> something. Instead of, I had, I had Grock build build a web page.

Rick Rodriguez

> No, that's cool.

Patrick Thomas

> I like it, actually. Yeah, it only took a couple minutes.

Rick Rodriguez

> I don't really like where I put it, put it in the root. I should, it should have been like, dropped, you know, but whatever.

Patrick Thomas

> Hey, Patrick. Yeah. You asked, you asked me to look at something earlier today.

John Mackenzie

> Do you remember what it was? Yeah, did.

Patrick Thomas

> I know you were going to do it.

John Mackenzie

> Did you get something going on with that?

Patrick Thomas

> Yeah, I think so. I just got to find it one second, one second.

John Mackenzie

> I'll just see if I can find it. Oh, that was an interesting conversation.

Patrick Thomas

> Whereabouts is it?

John Mackenzie

> I need to rerun it. just trying to think of where I rerun it from. Oh, that was the thing that dropped.

> My computer hit the wall again, and it did a restart. And I had a problem because I had to spin everything back up again.

> So it's not this one. It's over here. Okay. So I grabbed that, and then I dropped that over here, and that should go there.

> So what I figured is, so Patrick, tell everyone what you asked, and then we'll go from there. Okay. Well, I was showing everybody.

Patrick Thomas

> One of the first sites that I did, and that's how it came up, I'll show you guys real quick, it was, so this is all the stuff that's on my personal web server, but one of the first ones that I did was this one here, it's called Congress Tracker, and it goes in and it tells you, this is a public domain thing, and it tells you, you can pick all of Congress and just the Senate or the House, and it tells you what these guys are buying and selling on stocks, so you have an idea, you know, if you're looking at stuff, but so we, and I just threw that together because I remember I was watching, I forget, was like watching on YouTube or something, and some guy had created a site that was just following what Nancy Pelosi was buying and selling.

> Oh, that's what I was just going to say.

Rick Rodriguez

> Yeah, and he was mentioning, yeah.

Patrick Thomas

> So I'm like, oh, okay, cool. So I'm going to, you know, I'm going to just do that and Rockville built this, you know, and so anyways, and then I put the stuff that I invested in up at the top so I can always see where it's at.

> But anyway, that's how that conversation got started. And then there was me and John and Paolo. I can't pronounce his name, but the guy from here.

> Paolo. Paolo. Paolo was on there. And then we just started talking about it. I could see the gears starting to spin, man, in John's head.

> You see it. And then he was quiet for like 20 minutes while we were talking. I'm like, uh-oh, John's got another project.

> So what do you got? Let's see it. Okay. I'll just spin it up.

John Mackenzie

> Here we go. need to share my screen. So you gave this to me six and a half hours ago, right?

> Yes. What did you use, John?

Jobi Armstrong

> Codex.

John Mackenzie

> You're the king of cashboards. Right. So here we go. This is a paper only. It's going to be a simulator across the Australian Stock Exchange, the London Stock Exchange, and the New York Stock Exchange, right?

> Then what it's going to do is it's going to run, it's going to monitor, and I've got to do a couple of things to get it to the next step, but it's going to monitor a portfolio, so a test, a couple of test accounts.

> So you'll drop in money on a test account, then it'll run this like it's connected to a stockbroker, like a...

> So what it'll do is it'll run the method, it'll run simultaneous methods adopting whatever that method is, whatever the rules and the method is for that particular account across these three platforms.

> So it doesn't care where it does the trade, it's looking for the opportunity. So then essentially this will be your overview page.

> It'll monitor the live markets. So as the information's coming in, that'll just be your market page. It'll, you'll have your trade performance page.

> So this is pretty much trying to tell you how many trades it's done. And then how many have been successful versus, so, you know, in the money or out of the money, your realisation.

> So that's just your data page. And then you'll be able to, you know, bring up your... Your current positions, so that's what your current position is.

> So the whole idea is, you see in here at the moment, I've got a couple of, so I'm able to run experiments, because this is basically a simulator at the moment.

> The whole point of the simulator is to work as if it was a live platform. You're blanking out, you're frozen.

Rick Rodriguez

> Once money gets involved, the AI doesn't like it. Can you hear us, John? You're frozen. What platform do you use to trade, Patrick?

Patrick Thomas

> We have SpaceX through Edward Jones and the other one, and I inherited the other from the guy I used to take care of next door, though, used to take care of my neighbor, and he gave me that Charles Schwab account because, you know, it's got, like, and something else in it, and I had to mess with it, so.

> So, yeah, so I bought SpaceX when it came out, and then it dropped down to a, I originally bought, I forget, like, 18 shares, and then it, I got in, like, the day that it came, that it came out, and I'm like, and then I'm like, ah, I was watching, and it went down to $108, and I'm like, screw it, man, so I bought it, I bought 18 more shares, or 12 more shares, anyway, I got 30 total, so I'm like, okay, so cool, so I figured I'm just going to hold on to that for five years, and that's going to be my wife and was going to.

> That's our motorhome money, hopefully. No, that's the same thing I did. I don't have as many shares as you.

> have 10, but it's about the same process I went through.

Jobi Armstrong

> Yeah. I use Public.

Patrick Thomas

> Public is a really great trading platform, and they actually have their own bot system in there that you can.

Jobi Armstrong

> They have agents in there that you can talk to with and have agents help you out with the market.

> Really? Yeah. Public? Public, yeah.

Patrick Thomas

> It's a really great platform. I like it a lot.

Jobi Armstrong

> Instant money transfer, like you can take money in and money out pretty much instantly. Obviously, there's a percentage if you want to do instant transfers, but giving your money to the brokerage account, there's no fees.

> But taking it out, of course, there's a little bit of a fee. But what I like about them is it's not only just your traditional stock market, you can also do crypto in there if you wanted to, to keep it all on platform.

> However, I don't do that. I have. They Coinbase for crypto, but they also have savings accounts.

Patrick Thomas

> So they have a high yield savings account, which is 3.3 APY right now.

Jobi Armstrong

> And they also have T-bills, which are at 3.8 as well. When I first got into it, that T-bill was up to 5.7.

> So the interest on these savings accounts is actually really high. If you move a lot of money into their savings account, 3% is higher than most regular banks.

Patrick Thomas

> Thanks, yeah. Their bond accounts right now are 5.9% yield. So they got some good from there. That's cool, man.

> Is this just public.com or is it like? Public.com, yep.

Jobi Armstrong

> There he is.

Patrick Thomas

> He's back. Sorry, my internet dropped and I'm now… We were just talking about trades, so I'll put the link in there.

John Mackenzie

> Check that out, John. Yeah, I'll definitely kind of go check that one out. I'm just going to bring it up so I've got it half of the session.

> I got that from Jobi. I'm not getting credit for that. Yeah, I know. I heard that part of the convo.

> So, yeah, so this is going to basically be an experiment, right, so a simulator. So this will run the simulation until it gets to the point where – this is actually running right – Why, how come that's not working?

Patrick Thomas

> Segmentation fault on your local host? . I'm just trying to run it again, one second.

John Mackenzie

> As soon as I've got it working, I'll, there we go, let's just open it now. Yeah, so it's interesting because Patrick said like about six or seven hours ago, hey, go, you know, what do you reckon?

> And I, you know, so I built this in a little bit of that time. And basically it's going to allow me to run experiments.

> I'll just spin up a new experiment. Part of this experiment will have, and I'll do a little bit more work.

> I'm around this, but part of it's going to be linking to – so what I want to do is I want this experiment to link with an AI.

> So then I speak to the AI to research a method, right, and because this is a simulation – because it's a simulation, it's not going to be using any money, right, but it's just going to be following the marketplace.

Patrick Thomas

> And that's even better initially because I can say, hey, you know, help me design a new trial, you know, with this here, and I want it to be, you know, whatever these things are.

John Mackenzie

> So I can say – I'll go – if I go back and I'll maybe do a reset of that, I'll come back to the experiment, and then I open the experiment and say I want to speak to the AI because I actually liked the one that was there.

> And then I want this one here, and then I'll just extend it. And So that will then just say – and then I haven't connected this to Claude yet, but this is my next step.

> So this means that I'll connect it to Claude. Claude will go do research on a method. So then what I'll do is I'll run simultaneous methods all at one time, right, to try and find, you know, a position where it lands very high.

> So the methods all get mapped and they all get rated, you know, so you can come in and you can have a look at the rules that they're following.

> I think this can be expanded upon quite heavily. Once I get data – this is the brilliant thing, right – I can develop a method – because I remember speaking to someone about this the other day or a few weeks ago because once this is done, see, all stock exchanges have got like 15 or 20 years of –

> You movements for the whole time period. So what you can do is go to the stock exchange, you can pull down the data for the exchange.

> Some of them will probably have some APIs, pull that data, drop it into another database, then develop machine learning over the top of it, and the machine learning apply different methods to identify hallmarks of movement.

> This is what I'm going to do as I build out this experiment. They'll all get, so the methods will be created, then they will run the assessments and then develop things like lessons learned, so retrospective decisions that are made.

> So if you . If you buy today and you close it out, because it's trading, you close it out like in two hours or 26 hours or whatever, what you want to do is you want the AI to then document the trade, then develop the lessons learned, and the lessons learned might be over maybe seven days or 14 days, because trading is all about very narrow time positions, so the lessons learned isn't about a, you know, it's not an investment platform, it's a trading platform, anyway, then, you know, it's got its evidence data, then it's got its event journal, it's got its connections, which will allow me to then, you know, link it to the market, link it to my CloudCode laptop one and so on, and then it's got things like just the general settings and the profile and then the you know, AI

> You know, the feedback and so on. So this is where it's at at the moment. I've got to do a little bit of work about the AI intelligence.

> So probably link that to some type of – because heaps of people have created, like, investor skill sets and stuff, right?

> Heaps of those sort of things on Git. So what I'll be able to do is I'll be able to run a Git, scrape, find what I'm looking for, and then pull that into – pull that over here, and then, yeah.

> When you're doing a Git scrape, do you just write in plain English to your AI, I want you to scrape Git for this information, specifically this, and go and find me some stuff, or what?

> Sort of.

Patrick Thomas

> So at the moment, I don't do that very – I don't do that as well as it could be done.

> So I want to show you two things.

John Mackenzie

> I'm doing at the moment. They've both been highly successful. And both of them are just about to be improved.

> So this is basically intelligence gathering. Okay? So first one is this, YouTube. And I do this manually. And at the moment I've done it manually and I could do this far better, but I actually quite enjoy the process.

> This guy here is a brilliant guy. Has anyone heard of this guy called The Next New Thing? No. Okay.

> So what he does is once a week... that on YouTube? Yep, on YouTube. I'll grab it. I'll drop it.

> Yeah, I'll drop the link, yeah. So you want to follow this guy because what I get from him and others...

> This amazing stuff. I'll show you. I'll do that first. I should really drop it in, I'll drop it here, and then I'll drop it over in, what's it called?

> I'll drop it in Discord as well here, just in the general. You'll have to make more channels for the Discord.

Jobi Armstrong

> I can't wait. I really love learning about this.

John Mackenzie

> Have you ever used Slack? No, I've heard of Slack. I haven't used it. Okay.

Rick Rodriguez

> I know Slack's a Linux OS too, isn't it?

Patrick Thomas

> I don't know if it's built on Linux or not, but you can download it for whatever, Windows or whatever.

Jobi Armstrong

> Anyway, you should be able to go in and create as many channels as you want.

Patrick Thomas

> So doing like a YouTube channel or something like that inside your disk.

John Mackenzie

> Or something like links, useful links or useful... Links, yep. Yeah, useful links, so it could be anything because it could be a GitHub link as well, right?

> So, yeah, that would be very useful. I've got... Oh, my connection's still dropping out. So that's not... I've got that links, Jobi.

> I've got that links page. I should put that on the answers.

Patrick Thomas

> Because every meeting that we're in, I've got a bot scraping all the links, the human links that are dropped in.

> Well, if you and Rick get together, I'm sure you can port that into Discord.

Jobi Armstrong

> I'm... I guarantee you probably could.

Patrick Thomas

> I've got no idea. Because I've been doing it for a while.

John Mackenzie

> So Patrick, I'd be really happy for you and I to collaborate between your platform and this platform. Okay. So your platform becomes an intelligence layer, a signal intelligence layer over the top of this platform.

> That would, because that's going to give some, now I could go build it. That's not the point. I'd be really happy to do this.

> Because we've talked a lot about doing collabs, right? This is your idea. You just said, hey, John, go do it.

> And did it. So I'd be pretty happy to, it's got to get thrown onto, obviously onto a browser to then be tested, you know, from a public environment.

> And then I think a bunch of us could create, like. What? Test accounts and methods, and then because the more methods and test accounts that get created, the more machine intelligence will happen.

> And then as that – because what you're trying to do is – it's a lot like with my token saver.

> The more things I do, this continues to grow because my token saver is sitting up at 77.3% now. It's getting close to 80% on tokens.

> So – and then that's dragging up the cost savings. This is in Claude Code, of course. So as that's getting higher and higher – and I break things along the way.

> So sometimes you make progress and then you retract and then you fix the thing because you're layering more and more things on top of it.

> Because earlier today in the previous session, someone dropped Graft and they dropped the other thing. Yeah, the Gits, yeah.

> Gits, of the Gits. it was a head Yeah, Vroom or something like that, something like that, so I dropped that into my Claude Code, I ran an analysis across that, then I did a comparison assessment on what I know, what they know, where the white space is, where the overlap is, and there's a couple of things I'm doing overlap with them, and I think on one of the things, again, on one or two of the things, they're actually doing far better.

> So the same thing happened when someone dropped that one last week. The Viking one? The open Viking, someone dropped the open Viking, and it was like, man, I dropped that, I did exactly the same process, and what I found was that that was between 34% and 91% better.

> Like, I was getting 7% out, and they were saying 34% to 91%, so it's like five to 15 times better than what I was getting out.

> it, Thank My step, right, these two here are both, I can't remember if it was one or both, there's at least one of them that has got an overlap and it's better than what my step is.

> So I've built something already, but it's because I'm looking across the whole layer, they're only looking at one step maybe even in the layer of the vertical, and I'm looking at the vertical, the layers and that step, if that makes sense.

> So what they've done is they've spent all their energy on that one step in that layer, and I've got that one step, that layer, and the vertical.

> So I'm far better overall, and if all I have to do is just ingest their open source intelligence to improve that one step, and I maximize that step out, again, a lot like open biking.

> So I've got more development work, and the big thing on this one here, it was actually quite large. Uh.

> In Codex and Grok, the improvements in Codex and Grok were very large for those two things. So, believe it or not, I'm running out of tokens with all the different projects I'm dropping.

> I'm still running out of tokens. I still don't have enough. I've got to push some of those upgrades into Friday.

> My next week starts from Thursday at 9pm my time. So that's like in like, I don't know, like 15, 16, 17 hours.

> So I've got one computer I need to burn tokens on, but that's a different story. Anyway, so I'd love to do some co-lab on this.

> I'd love some other people if they've got ideas around, you know, the AI intelligence stuff. Yeah. Where was I?

> I'm going to do that. Yeah, yeah. Look, I'm very, very keen to, you know, to run this. And, like, me just putting JMACTrade, that can be named anything, you know.

> Anyway, what we were talking about was the Gids. Okay, the Gids. So come here, go to this guy. Every week he drops 10 repos that are awesome.

> Oh, this one, he is all just about token usage. That's going to be a good one to watch. But there's another one.

> We want to have a look at this. That just dropped. We lost your screen, John. I just said an upgrade on a show.

> While he's looking for that, something that's really useful I do a lot, I should share my stars with you guys because I star a lot of repos, but a lot of times I'll put a repo in that.

Jobi Armstrong

> I'll see you guys. you. Is similar, or that might benefit my project, and instead of forking or copying the repo, I'll just ask Codex or Claude to look at the repo, do a deep dive, and tell me what's beneficial to my project and how I can use it inside my project.

John Mackenzie

> Yeah, that's part of it. I never fork, and I never start, I never fork. Right. I start, it saves it, so I don't have to go back and keep searching for it.

Jobi Armstrong

> That's the reason I started.

John Mackenzie

> Yeah, I don't, because that gives intelligence to anyone that's observing me that I, what I'm liking, and I don't want anyone to know where my intelligence source is coming from.

> So do you clone it, or how do you, what do you do? Um, well, I'll see over here. There's a lot of kids, a lot of kids, um, in.

> My OneTab over here is starting to populate, right? See Archify, Archify, you've got the Codex Cortex, the Body Mind Systems, Codebase here, System Audit, Secure Flows, Aluva for GRC platform, they're not GITs, those ones.

> This one, here's a GIT, Baladar, Headroom Labs, Graft. So what happens is someone will say, here's the GIT, like this one here, and then what I'll do is I'll just save it through my OneTab, and then I know that's where it is, so I don't, when I open up the GIT, I then save it to my OneTab.

> What is OneTab? I don't know if it was paid or not, but basically, I'll show you what it does.

> Saves your tabs or...? Yeah, just save it to the tab, so you can close And not leave them open.

Rick Rodriguez

> So, yeah, that's what it does. And it's just an extension here.

John Mackenzie

> So I could build that in, like, 30 minutes. That's so easy to build. It's not funny. Anyway, that's a different thing.

> So go to him, watch his stuff. Once a week, he drops with this other guy. I don't know if it's that guy or a different guy, but they talk about, you know, they're about 15 minutes long, but they talk about the – you can't see my screen.

> They talk about the – that week's always 10 gits for that week, and it's, like, highly starred gits or highly, you know, interesting gits.

> So I find that I've only just started doing that. Now, the other thing that I've done – I'll show you this here.

> I think – now, this here, I think it's pretty cool. Are you ready to – Are blown away? I'm ready.

> Okay. Are sure? Are sure? I'm sure. It's this one here. Right. Hello. So what I've gone and done is I've scraped, I've got access to this database of 18, nearly 1900 AI users.

> Like seven, okay? Here's my data. So I've used 306 billion tokens in my last 115 days. So like in my last 71 days, you know, it's like, that's my token usage.

> So enormous amount, right? So then what I've done is I've, I've got the all time users. So, and then I can, I've two, the top 200 because after.

> After that, it doesn't matter, right? So I've pulled down the top 200 users, and then I've had to pull a dashboard around it so it can tell me, like, what their weekly, what their monthly, what their all-time is, and then what I want to do is I want to see where I sit in comparison to them.

> So, for instance, this month I'm probably on target about 130 billion tokens, but I'm going to cut back one of my Claude accounts.

> So that's probably not going to materialise. But my all-time, you can see where I sit against these other users.

> Now, part of this is you can sort of drill into it. So I've built the dashboard so you can drill.

> So I always like drill through, and I also like filtering top 20, top 50, top 100. So I can start to see what the top 20 users, what models they're using.

> So... So if I look at the top 20 users, as an example. John, where do you get the users from?

> How do you know that they're top token users and stuff? How do you?

Rick Rodriguez

> Oh, I found a database with it. I could try and dig out where that was because I've stopped going to the database because I'm just tapping it through a connection now.

John Mackenzie

> So I can go figure that out. So then because I've got all their users, right, and I'm still building on this at the moment.

> I'll show you what I'm building. So this user here, he's like a prolific user, right? So what I want to know is this.

> I want to know who is he, right? I want to go to his GitHub. I want his GitHub, right?

> See how quick that was, right? But what I want to do is do this. I want to pull intelligence.

> So I've just... I've built a system where I can pull intelligence from this dude. This is what he's doing on GitHub in open source public.

> And now he's built all these repos, right? Now what I want to do is say, well, what repos are you using?

> What's his name? Penberdo, whatever, right? So now what I'm going to do is, what I'm doing now is saying, okay, which one of these gits is interesting to me or are they all interesting, right?

> So what I'm going to do is I'm now creating, which it's not working properly, something called intelligence. It's still not working, where I can pull down using not AI, using CPU, right?

> See how I transitioned? Now I've built something using AI and then I've now got a CPU machine. Um, um.

> It'll be scheduled and do polling, which it does daily, but I can do that at any time. So I can just press the button, and then it just runs an update.

> Is that your own CPU, or is that the GrokBot CPU? This one's just my own, because, look, I'm just having a problem.

> I'm running a test at the moment, and one of my tests fail. I've ran a number of tests using GrokBot.

> VPS has been failing. That's good, because I'm actually figuring out the limit of its capacity. So over in my, oh, this would have stopped because of my, my, so I'll just say proceed.

> Oh, no, no, that stopped because of a different reason. Sorry, I just saw the little red. So. it somebody ?

> So I was running, I'm running tests over here, right, on, basically I'm running these tests on here to see if I could, I was trying to see if I could get my codex to tap my GrockBot, to tap the VPS, to manage multiple small LLMs in the VPS.

> Did you follow what I just said?

Patrick Thomas

> You're loading small, small little LLMs to just do the grinding work, just the grunt work.

John Mackenzie

> Right, so, and I was failing getting a lot of stuff done here, so then what I had to do is I had to jump over here, I dropped my requirement here, and I'm having some issues with my GrockBot at the moment, so I've got to come back and spend some time on here to see if GrockBot can, because one of the issues I had is with my codex.

> Zero.

Patrick Thomas

> I had this codex connect to my Hostinger VPS, and when I had it run the first test, it got confused for like an hour or so.

John Mackenzie

> I was running these tests, and I ran this, I ran LAMA 3.1, the 8 billion parameters, and it failed, and it wasn't operating, and it said it was struggling, and eventually it said it only had access to four CPUs or something here, right?

> And it was like, no, no, that's not, that's not right, and it's like, man, and it said, it said that something else is useful.

> It's using the VPS, and it's in production, and I'm thinking, okay, well, I'll jump over to the bot, and I cancelled my, because I had two GrokBot sessions, and both the sessions that were tapping the VPS over there to run the research I was doing over there, I had them both cancelled.

> Yeah, we like your screen. Yeah, I'm just talking. So I cancelled it, and then I thought, okay, they're good, just cancelled, I'll come back over here, I'll get Codex data to tap GrokBot, and then it's VPS, and then run the trial again.

> It's running the trial, I come back over here, and after about whatever time, it's saying, hey, it's still in production, I'm saying, it's not in production, I've just cancelled over in GrokBot.

> Anyway, so I went back to GrokBot, had it run a test to see if it was cancelled, yes, it's cancelled, come back over here and said, hey, no, it's definitely cancelled, run it again.

> Watching it, you know. So with the feedback on the screen, and after a minute or it comes back says, no, no, it's still in production.

> So I stop it. I'm waiting on it, and then I'm going, it's not still in production. So I had it write a prompt, take that prompt, went back over to GrokBot, dropped it in GrokBot.

> No, it's not there. Had it run its GrokBot doing analysis, picked that up, come back to Codex, drop it back into Codex.

> And it was my hostinger VPS that it got confused with. I'm giving it explicit instructions, go to GrokBot, use the GrokBot VPS, and even, so this is Sol 5.6 medium, all right?

> So Sol 5.6 is one down from Astra, right? It should be, like, it's a, it's a, it's it's a frontier model.

> It doesn't need, like, beyond medium capacity, and it failed time and time and time again with explicit instructions. Go to GrokBot, use the GrokBot VPS CPU and run this test there.

> Three or four times it failed to follow the instructions. It was using my Hostinger VPS that I gave Codex access to two weeks ago when I was running a split test, A-B test.

> Then I said, and then I said, because it's come back and said it's using, like, one CPU, and as soon as it said it's using one CPU, oh, actually it said it was, it had 3.8 gigabytes of memory of RAM, and I'm going, no, no, no, no, GrokBot's got 16 gigabytes of memory.

> That led me down the path of discovering that it was using my host into VPS, and it was not using GrokBot.

> Then I said, okay, after I discovered that, can you tap the VPS from here? No. So Codex, and this means Claude Code, I imagine, can't use the VPS remotely.

> Then I said, can you speak with GrokBot to tap the VPS, and it said no. So then I had it write a prompt, take that prompt, go over to GrokBot, drop that in to run the trial, to run the test to see if it works, and that's where I'm at at the moment.

> So everything we do is about running these types of experiments because what I'm essentially trying to do is see if I can spin up two or three small LLMs on the VPS.

> And what LLMs are you using? The three that I'm running the trial on, one was Lama 3.1, the 8 billion parameters, that was one of them.

> One is a 4 billion parameter or 3 billion parameter and a 1 billion parameter. I don't have those both on hand at the moment.

> They're all U.S. models. So none of them are, I think one might have been a meta, the Lama's meta.

> How are you? Are you accessing them through OpenRouter, or how are you getting a hold of the LLMs? Are you going direct?

> No, Codex will do it. So Codex is grabbing it. I'm not even, you know, so basically I'm engaging with my soul to run the analysis, the research around the small LLM list.

> I've got a different chat. So here's my chat. And, look, I ran this chat in ChatGPT. So this analysis was not in Codex.

> This chat was in GPT, right? So I'm not using any Codex to do the research here. I'm 100% different bucket.

> And then essentially what I landed on, and because it's got, so I'm still running some split tests with GPT at the moment.

> question slide. Because GPT and Codex obviously can connect to your GitHub, so I'm trying to determine at the moment, which I haven't landed on yet, that if GPT taps GitHub, is it transitioning to work and work uses Codex, right?

> So I haven't landed on that yet, but one easy test now would allow me to know that, because it's important to realise, because if you can push, say, all of your research questions into GPT, right, and use zero coding AI inference, you've protected your AI inference to do code, work, or whatever work that sits in that.

> And then all your research sits within, like, another vertical, like a GPT, which I've never capped out and I've done so much work in a GPT, right?

> So what I'm working at the moment is not just maximising the token savings, I'm not just maximising a code use because I'm trying to work out how I can push all my research into the, like, you can't do it with Clawed code or Clawed because in Clawed, it's still using your code inference, your AI inference.

> So you're hooking those three LLMs into Codex? No, so at the moment I'm... Codex is using it. Ah, so at the moment I'm figuring some stuff out there.

> I haven't landed on it yet, but you can see where I'm going. But what I'm looking at doing at the moment is, to put it in three distinct buckets, I guess, is the first one is my token savings, which you've heard a lot about.

> The second one is, can I drop LLMs and do something interesting with them into a VPS that does something that's going to be really interesting?

> So I'm running experiments across that at the moment, and at the moment I'm trying those experiments explicitly in Grok, Grok's VPS.

> I haven't landed that yet, but I'm still working through that. And then the third one is, with bodies of general research and stuff, can I move that out of the coding LLMs, right, out of Claude Code completely, and say Grok or Cursor completely, and drop and out of Codex completely, and put it in ChatGPT.

> I'm working by Kводx. that Thank Specifically because it is segmented from my codex limit, so that means I get unlimited research, right, and oversight and everything that doesn't tap my code, my coding limits.

> Does that make sense?

Rick Rodriguez

> Yeah, but with the GrokBot, if you're using the VPS, isn't it still, by using that VPS, isn't it still using some kind of usage through Grok?

> Ah, see, I've solved that.

John Mackenzie

> That's coming down the pipeline. So I solved that a little while ago. I'm still fixing that there. So, yeah, I'm just trying to figure out the small LLMs at the

> But I see where, I think I see where you're going with that. I mean, you can hook that in either through an MCP or a webhook.

Rick Rodriguez

> I'm thinking, and I don't know exactly how webhooks, because I haven't used one myself, but they use, but in, I mean, if you use a webhook because there's a Chrome browser in there, could you kind of go through the webhook through the Chrome browser to the VPS?

> don't know if you can use that way or not. I'm just. Yeah, look, to be honest, I'm not certain which way that's going to drop at the moment.

John Mackenzie

> I'm still running tests across that. I've got pathways, I know it's going to work, but the exact way that that's going to work, I can't tell come in through the browser through a webhook, if that's possible, that's another way into the VPS.

Rick Rodriguez

> Yeah, look, I don't know if you can do that with.

John Mackenzie

> But I know, and I did have Cloud AI work. He in the Chrome inside the VPS2.

Rick Rodriguez

> Cloud.ai was working in Chrome because I installed the Cloud.ai extension, and he was actually working the Chrome browser in the VPS.

> So are you talking in Grok's VPS?

John Mackenzie

> Yep. So now say that again. Okay. I installed the Cloud.ai extension in the Chrome browser in the GrokBot VPS, and it was controlling the browser.

Rick Rodriguez

> It was controlling things in the browser. That's interesting. Is there a reason you did that?

Jobi Armstrong

> Can't GrokBot reach out to the browser and control it? I was actually just trying to, I was just using it in there to try and create that Discord bot.

Rick Rodriguez

> That's the, that was the whole reason I put it, put it in there. I didn't even. Think about, you know, just GrockBot may do this in the browser, but I thought I would use Claude, and it worked.

> It just had, it logged me into my Claude Anthropic account and started going to town. I'm just wondering, putting Layer on top of Layer, and I'm just wondering.

Jobi Armstrong

> Yeah, it might have been kind of redundant. And you could either just do it in GrockBot or do it in Claude.

> Yeah. But it's cool that you could do that, I guess, because it's just agent. It's cool. It's good to know, I guess.

Rick Rodriguez

> What I was thinking for John's instance, I don't know how webhooks use, because I haven't used them before, but if you can, one of the things is if you can get in that way and use VPS and inference and everything and connect your ChatGPT or your codex in there that way, I don't know if that's possible or not, but just an idea.

> Well, I've got an interesting use case at the moment.

John Mackenzie

> And like a... I'm just going to run another test in Glockwad at the moment, but I'm running multiple tests at the moment because I'm actually building some infrastructure with the tests that I'm using.

> But let's get back over to the GITs. I'll show you what I'm doing with those GITs. It's quite interesting with those GITs.

> What do you want to eat, buddy? Oh, sorry, yeah.

Jobi Armstrong

> Oh, it's this one here. Okay, so I've got the top 200 guys, right?

John Mackenzie

> I've got, so I can go to any one of them, right? This guy down here. And this, no GitHub linked, right?

> So no access. This one here, no access. So I probably need to do one where it only shows up.

> to to Thank Look the guys that's, well, in fact, intelligence, one of the things that this actually does is say, hey, these are the people that's got their gits.

> So if I say all the 200, it just says, well, these are the ones that's got their gits. So, okay, so I can say with this person here, right, this is, I need to run this better, but this is what this person's working on, right?

> So here's his top repos that this person has. So, for instance, what I can, because I've now got the intelligence of these people that's using massive amounts of AI compute, and I know that they're harnessing massive amounts of GitHub, right?

> I can then pull together all the, all the gits that everyone's using, both this. So, let's see. The gits that they've starred and the gits that they've – the open source gits that they've created.

> And these are smart dudes, right? Sorry. These are dudes that are using lots of AI tokens. So what that means is I can now – that's why I'm building this intelligence layer out here because I'm – it's like I'm now building a dossier on these people of their – the part of the tech stack that I can see that they're using, right?

> So I can then pull of that – pull of those gits to find is there gits that they are using?

> Can I see that? Yes or no? I have not experimented with that yet. The second part of the question is I do know the gits that they've pushed to open source.

> Have any of these people created anything that I would find? And useful, either in its raw form or when I scrape their, so a lot like what Jobi was saying, which is what I do, as I said, I never fork, I never star, but when I scrape their, that repo, what does that repo tell me that they are doing brilliantly, that I need to know, that I don't know, it's not in my, intelligence or things like lessons learned, or I'm going to build an intelligence layer that picks that up and documents the brilliance of the people that's sitting in, you know, some of these spaces, and then pull that intelligence into a new layer of, A, if I want to build something, leverage the Git idea, leverage the concept, leverage the, the, the, the answer.

> Architecture on how to build something and the best ideas they've got within that repo. Yep, that's awesome.

Jobi Armstrong

> Now I understand why you don't star because that would put you in your own database, essentially, because you're a Yep.

> So I'm already a top user.

John Mackenzie

> I don't open source anything, right? And I don't open source anything because I want to make money, right? So I don't want to give it away.

> But if I star it, I'm leaving a breadcrumb. I get it, for sure. And I don't want to leave any breadcrumbs because what I then get my agents to do is when I get – because when it's open source, they can star it, they can fork it, or they can read it.

> And in the reading, as you know, They can still find everything that they need to in the read, right?

> So then you can say, copy it, and they'll say, hey, I can't copy it because they followed the rules, right?

> They say, hey, I can't copy it because then they've got to have attribution. You don't want to give attribution, right?

> So it's like, okay, rebuild it and make it better. And right at that point then, that can have a few bugs in it.

> So that's not perfect because if you fork it, you're forking the evolution of improvement, right? But the problem with forking it is you're giving people knowledge on perhaps how you built something or you have to give attribution into the future forever, right?

> and the, and that. So I would rather get my – find the best, the brightest, the smartest, copy better.

> So that's what I do. This here is a new – you can see I'm working on it. This is in flight at the moment.

> It's not perfect yet, but it's on the way. Then what I do is I want to have, like, different ways to look at these things.

> You know, what technology they're using, you know, and you can see I'm using God's EyeView. I'm using Archify and I'm using Semantica.

> Oh, you can't see it. So what I'm using is other gits, right? Hold on. Back up. You're interested in God's EyeView as well?

> Oh, yeah, yeah. I'll show you something I've just built, something I've just landed. What is God's EyeView?

Rick Rodriguez

> Oh, man, it's a pretty cool job. Oh, yeah, yeah, yeah, yeah.

John Mackenzie

> I'll show you. I've just built something with it. I love it. And. I'm a huge fan. It's this one here, this one here, here we go.

> So you know my website, right? I've just combined God's Eyes View with Symantica and Archify. Archify is good, too.

> Yeah, and this is what I've created. Yeah, that's sick. Right, so you can come in here now and you can say, hey, I'm in Australia.

> You can now see the library of documents that I've got, the assessed companies that I've got. So here's the 11 assessed companies at a deep dive level that I've completed.

> You can't drill into them because you've got to pay for that. But you can fly to Australia, right, and now...

> You can actually see that that's Australia right there. It's got 11 documents. It's just landed, so it's not actually scrolling out at the moment.

> I'm just going to tell it to scroll out. But this is my live corpus. I've got 42 jurisdictional documents.

> I've got 546 company entity assessment deep dives. I've got 149,506 42-point entity scans, 109,000 companies, 16,000 different company scans, and 133,000 PET scans, right?

> Oh, so there you go. It is going out. So then what you can do is you can look at it through the different layers, the jurisdictional layers.

> You're looking at it through the entity layers. You can look at it through my Blackstone Intelligence Zero Trust PET scans or through my BSI layers or my five layers.

> And like... With every one of these, so as an example, you can then scroll in and see in which countries how many scans have I done per country, right?

> And this is all – you see this here? This is mapped. I'll show you. So if I come over to my, say, BlackSnow Intelligence, right?

> Oh, no, I don't want to do that there. So say I want to come over to – oh, this one here.

> You guys would want to go – you're going to want to go use this. I got this from – Selena?

> Selena, yes. Sorry, thank you for that. So you can see my pet fired because it's live. Then I can jump to the evidence, right?

> So if I jump to the free BSI calculator, so this runs. Automatically as you do that, okay, that's finished now because I know it's finished when it comes up with the red across the top.

> Okay, so that one's done, so I close that down, and then I can say, give me the five layers.

> Now, you watch these five layers when it's completed the scan, see this scan of five layers here, right? Now, if I go back to my wherever it is over here, here's the five layers here.

> So this is the five layers of, it's all integrated. So I've created something that... That's pretty sick. And then, then you can go, rather than look at it from the, you know, from here, right?

> Is God's eye view just the globe, or does it do other stuff? Oh, I don't know, it must do some other stuff, but...

> Go to the chat, there's in the chat. Let's see. I'm So now I posted the original creator of God's Eye View in the chat.

Jobi Armstrong

> He has a YouTube channel showing everything it does, and it's an open source as well.

John Mackenzie

> It's an open source gear. So you can see that I've now got this embedded into my website. So I've got my globe.

> I can go flat. And then what I can do is maybe it's a jurisdictional level. I can then do this.

> So say you're dealing with the GDPR, you can start to trace how these different acts are affecting your privacy rights as a person, but also as a company.

> So is that where the data is flowing to and from all those different?

Rick Rodriguez

> Yeah, so basically it's given you insight on some things that you need to consider.

John Mackenzie

> You know, you've got to pay for it in some ways, but, you know, so essentially this here is – that was an upgrade to my page, that block that you saw.

> So because I had this, which is live, right, but now that is basic – so I could probably delete this now, this block here.

> Live from the corpus, because now this block here has got – so if you have a look at all those stats there, those stats are the same stats that's here, right?

> So I can – I probably won't delete it. I'll probably just hide this block here because I don't need to repeat it, and, well, there you go.

> know, that's all the different countries, you know, in the – In the corpus, it's all the different companies. So, and you tell me, what do you think?

> Very slick. I like the interface.

Rick Rodriguez

> It's pretty sweet, man.

Patrick Thomas

> Very cool. So that just dropped as we started to chat there.

John Mackenzie

> So, you know, I think there's a couple of things I need to do. So having two information, and that needs to be Hover.

> I always have them on Hover, like information things. So that's not working. And then, you know, this one, here's like the lenses.

> So that could be combined into one information. So it's just little things, right? So anyway, yeah, that's sort of where I'm at at the moment.

> That's now ready to go. Yeah. Do you have like a, I know that you, you had SEO business.

Patrick Thomas

> For quite some time, do you have like a website that you're promoting all the software, all the stuff you're writing so that you can sell it?

> No, I did a little while ago, I did something called JMAC Tech, JMAC Tech here.

John Mackenzie

> I mean, you have all this cool stuff, I'd like you to see start getting paid for it.

Patrick Thomas

> Yeah, look, so JMAC Tech is a little bit where I started to put all my projects onto one page, but I've done so many more projects.

John Mackenzie

> I was the apps page where you can start to see the apps. But this was like done like two or three months ago.

> It's got nothing, you know, compared to what I'm doing at the moment. I also, I upgraded my, because I think I showed it earlier that I can teach my JMAC learning.

> So with my JMAC learning, I'm a certified trainer for ISO accreditation.

Patrick Thomas

> So... .

John Mackenzie

> I worked with ISO 27001, which is Information Security Management System, so cybersecurity, ISO 31000, which is Risk Management, and ISO 42000, which is Artificial Intelligence Management System.

> So I'm a certified trainer for global standard certifications for those ISOs. So basically, what I did is I built this, pushed it live, and you can have a look at the domains that I train people in.

> So I built this, oh, you can't see it. So I built a website that sort of shows that here.

> And, well, this is all the, I train 40, I can train 44 certificates. People can buy and then get global, that drop already, wow, global.

> So you can actually see that, you know, I built this for my website, so for cyber, for risk, for artificial intelligence, that's a little bit better, you can sort of see it there.

> So you can start to see that this is fairly as well, I think. So, yeah, and then you can sort of decide, you know, what, or you make a selection on sort of, you know, your journey of certification.

> So then I'd sort of, oh, that's the flagship sort of certificates, all certificates that I train. So, you know, that's a public website, JMAC Learning.

> Now, to your point, hold everything on my projects. It's one page because it's just too much to manage. So this is like internal use, so I entered my own hub, and I think, Patrick, think you inspired me to probably do this watching.

> I think you had a lot of stuff on one page, you showed a couple of times, and because you did that, it's like, man, I should do something.

> It's completely different, obviously, but I should do something similar. And look, I've got a lot of projects that's somewhat out of control, where they've got lots of sessions.

> Those sessions have got gits that may have been pushed pre-prod, but not merged to main, right? And then it's like, how do I manage that?

> So what I did is I wanted to get all my projects onto one page, which you can see there, that's one page, and to say my JMAC projects, or say my...

> AI engineering operating system, which is a major focus at the moment. So these are the projects sitting inside that, right?

> So, the sessions sitting inside that. So I can say, hey, this is my cybersecurity scan project. This is what's happening in that project.

> So I've got 17 pre-prod GitHub commits that need to be worked out. And I can't figure out where that sits within the, well, how am I going to merge all that without any conflict?

> So now that I've got this to a point I'm happy with, I'm going to then have a button down here, and it's on the way, but a button down here that engages an AI-skilled LLM that's going to look at those commits.

> In the pre-prod, and work out a... It's safe way, a safe strategy to merge everything that needs to be merged to Maine safely without any conflict.

> So that is going to be built into this here. So then I can remove the issue of the – because if I go and have a look at my overall, you see my overall.

> I've got three things that need my attention, 18 that's on the watch list, and I've got like all these sessions, right, that when I enter into here, I've got major problems, and what I'm trying to do now is just clean up and fix up.

> So this isn't a code-based review. So what you were talking about earlier, Jobi, this is like just a mess of commits that's sitting in pre-prod that needs to be, you know, merged in the Maine safely and make sure that there's a QA assessment over the top of it.

> So I've I did did is I built this. this. So So And then I want to see it through different views.

> So this is my AI engineering operating system. And then I want to look at it based on cards. So where is it?

> So my AIS has got a local host. So then I can come here and say this is that. So that there.

> Right. Oh, sorry. That's my cyberscan. My cyberscan's got a local host. if I want to find something easily, rather than trying to find it through one of my tabs, I can close a bunch of tabs down there because now I've got access to, I know I can access the repo.

> I can see what's been pushed. I can, I can open the session. I can open that and then click through to the session, or I can just go to the, you know, to my, my cybersecurity platform.

> And this is my cyber platform. So if I, if I ever want to demo anything, I can say, well, here's my cyber platform.

> This is what I built. It's been running for, you know, 90 days or whatever. And I can close it down without worrying about it because I know exactly where it is.

> I can do the same with, as an example, with my AOS web. So with my AOS web, this should be showing here that I can, because AOS web is here, right?

> That's what it is. So I will go back and say, hey, that's not connecting. So I've just got everything on, you know, one pane of glass, so to speak.

> So that's what I'm, that's what you sort of inspired me to sort of fix up, Patrick. Cool. Thank you.

> I'm glad I inspired you.

Patrick Thomas

> I did something for what we were talking, you know, with the links and everything. I just, I added it while we were talking.

> Stay going. I just want to show it to you guys, and then I'm going to, like I said, get with Rick on this, but I don't know if you guys ever heard of, it's called, let me show you, let me show you what I did real quick, what's this, so here's the thing he was talking about, this is all the stuff on my local web server.

> So this is what I had to do, I don't know if you guys have ever seen this, the Symbaloo website, I told it, go,

> I just want to show it to you guys, and then I'm going to, like I said, get with Rick on this, but I don't know if you guys ever heard of, it's called, let me show you, let me show you what I did real quick, what's this, so here's the thing he was talking about, this is all the stuff on my local web server.

> So this is what I had to do, I don't know if you guys have ever seen this, the Symbaloo website, I told it, go,

> And kind of, because this is, if you look at Symbalude, I ran across this like a bunch of years ago, and it's like, and they do, they do it like this, you know, I'm going to skip to them, but they do it like this, and you can create different things.

John Mackenzie

> So I told GrokBuild to use, kind of look at that interface. But one of the things that's cool is I made all these things searchable now.

> So like, if you want to, like, one of the things is Ponychail, I remember, so click on Ponychail, it'll take you right to it.

> You go back here, all the tiles, and then you can go into this week, and these are the ones this week.

> Here's the archives for August and September, you know, but they're searchable, so I don't know, it's, it's a little better than it was.

> Thanks.

Patrick Thomas

> Patrick, you're on something with that, because back in the day, when I had my graphic design company, a couple of things I often would do is look at fonts and font families, and then also look at icon, so iconography, and then I'd be looking at the iconography that I wanted to use as part of some type of development, whether an app or whether it be a website for either me or for someone else.

> And, like, there's a bunch of free tools out there for those sorts of things. So to make the apps even better, you can actually go find some of that tooling and then just point your app find find of tools in the

> You know, when it's been created, you can then just point it to some families of the iconography or the fonts, so it just makes it even easier.

John Mackenzie

> Yeah, I'll say, I mean, I haven't used this for years, but I got a job at, like, it was a data center, like, in 20, I only worked there for, like, six months.

> Hey, John, that's what I did for my little CW on Cortex Works. I've got a bigger Cortex Works, but I used a font family and created that, my little CW.

> Oh, nice. Yeah. This is the original, this is the assembly website, and see, you can create tabs at the top, and then with, like, data networks, a place I worked for, these were, like, all the links that were used for that.

> You know, I did one for, like, admin tools, IT support, you know, marketing. Patrick and Will, what I'd do if I was one of you guys, because you've both got a partial view of what I've already said, what I'd do if I was one of you guys is I would create – Uh-oh, those gears are turning.

> Those gears are turning again, man. Yeah.

Dr. Will Fisher

> What I would do is I would create a website that pulls different sources, different families together.

John Mackenzie

> And you can do this deterministically, right? Because this is more like machine process rather than AI. You build it with AI, but then you do it with machine, BPS machine, then I would pull it into a website and then I would look at things like fonts, iconography, even colour theming, find a few other things, right?

> can tactics than So What I choose Kurds All onto the one website, and then I would put AdSense over the top of it.

> This would be sort of a one place somebody could go and create their logo or their icon or, but then AdSense, so that potentially that they would click on something else that would make a little money.

> Yep. That's interesting. Okay. Because what you're doing, you're just having a website, a free website that becomes a fountain of all the, all those families of knowledge.

> And then what you want to do is you just want to, you want to go to Google, you want to go to like your chatting for tea or whatever and say, find me the top 50 sites that does that, find me the top 50 sites that does that.

> And then what you do is you pull it, you pull it through an API or through a database or scrape, whatever, and pull it all onto yours.

Dr. Will Fisher

> Because even the thing that you want to do is you want to,

John Mackenzie

> Whether in bed, you don't want to scrape it and steal it. You want to attribute it, right?

Patrick Thomas

> And then you build that site to become the powerhouse of whatever it is. You could do this with anything, by the way, not just those types of things.

> Yeah. Yep. So that's what I'd do.

John Mackenzie

> I would, you know, because find things that people search for and then see if there's sufficient data available for those things and then build that interface that people can find it more easily or tap it more easily from yours, right?

> Put an MCP, make it AI friendly and then put an MCP connector across the top.

Dr. Will Fisher

> So then all the agents can actually tap it.

Patrick Thomas

> So, yeah, I'd be really, really creative in how I'd go about that.

John Mackenzie

> That might be beyond my skill level at this point, but I like the idea. I like the idea. I mean, I like making money, but I mean, if it's something with the AdSense where you promote products on there or something, you promote or sell somebody else's stuff, is that what you're talking about?

> Yeah. So Google AdSense, just Google, just, you know, research it through your AI, right?

Dr. Will Fisher

> And it'll tell you everything you need to know. Okay. It's a monetization pathway.

John Mackenzie

> I was thinking Claude could help me figure it out. Like it's not, it's so amazing now that literally if you just start asking the questions, it'll help you figure out what you're trying to do.

> Absolutely. Yeah, I like that answer. Okay. You know, because think of, um, The monetize, you're building it once, and then what you want to do is you want to create a bot that creates blogs for it, because you want to get SEO, AEO, and GEO growth.

> So it would be potentially like blogs on color, or blogs on fonts, or blogs on, you know, how to choose your icon, how to choose your, yeah.

> But I would do align things with it as well, because when I had my design agency, I found that a lot of people didn't understand things like, what does the best, say, graphic design skills, what's the skills, what, what, what's someone with a great graphic design eye look like, or what do they look for, say.

> So you're looking at margins, paddings, you're looking at like the thickness of lines, are they circular or curved, are they all these things, right?

> Now, you would be able to drop in blogs that you pull from YouTube, right, because there's experts on all that stuff on YouTube, and they're going to give you this richness of expertise.

> Now, what you do is you find them on YouTube, very easy to do, right, you can even get your agents to do that, find the top 50, find the top 100, use the LLM Cortex, pull them into the old notebook LLM, drop 300 into one, you know, one theme, whatever it is, then write, you know, 20 blogs on different components.

> 30 blogs on different components of that theme, get a video created on one part of it, and even if it's got notebook LLM down in the bottom part of it, the video, the audio, the presentation and the one-page document, the one-page landscape, you can drop all of that onto your blog, right, have that all for free, have it transcribed, the video transcribed and the audio transcribed, drop that into the bottom of it, man, from an SEO point of view, this is fantastic stuff, right, so that's what I would be doing if I didn't have any major projects to work on, because you can build out, and then you can automate all that, you can work on how to, you do it yourself, you know, for maybe the first 10, first 20, because then you've learnt the process, you actually know it, you've become an expert in something, like doing that process, then what I would do is I would then

> Work with your, you know, with your, the flavour of your AI to build out an end-to-end system that just does that one thing, just that one process of blog creation, which Keith's already done a lot of work in that space already, right?

> So then I'd just get that, that's just going to do your blogs, and that's going to get you, over time, your SEO, your AO, your geo, right?

> But, but that, that's the, that's one part of what you're doing, because what you're trying to do is, it's all those families of stuff that you've bought in that is generally open to the public and open-sourced, right?

> And then that's one, that's one idea. Think of a system idea that can do that, right? So you, you, you, just build out these ideas of, and then you, you, you, what I'd do is, I'd build, um, not only the AdSense, but then I'd build a calculator, or calculators on top of it, so then what you do is, you, because you,

> can build out like an end-to-end calculator, show you what I mean with a calculator, right, and Claude Code built what I'm about to show you, and this one's a very big one, very sophisticated, but Claude Code did it, it was on my business intelligence, and here I've got an ROI calculator, right, so you come to your ROI calculator, and then this is it here, you can put in your name, the JMAC, all right, and then you can build whatever your process is, but this is like super sophisticated.

> Yeah, I don't even know what I'm looking at. It's like it's a very big calculator that helps people understand, and then like here, see that?

Dr. Will Fisher

> You can build calculators like this for anything, right? So I know that someone built just a page of calculators, right?

> And they put like 50 or 100 different calculators on one page, and any time someone's searching for something, they want to get this easy thing.

John Mackenzie

> So what they did is they built this calculator page, and that was their, like the blog to the SEO, the terms that someone's going to search for whatever it is, right?

> And then they just built calculator after calculator after calculator, all different versions doing different things. But you can now build these calculators out in any way with any graphic representation, right, and then monetize it.

> So you could, let me just guess, so you could do like a, which I think I've seen on here, like an ROI calculator, you could do some sort of financial calculator on here, you could do, you know, converting pounds to the U.S.

> dollar or something, like you can basically calculate anything, but then the SEO would all come to that page and then those folks could get that information.

> Is that what you're talking about? Yeah, absolutely. And what, so what you could do will, so that's one particular pathway.

> Now think of just the general, so you could, so you could build an SEO calculator that, that does something like this, right?

> Put in your URL, your company, five competitors, right?

Dr. Will Fisher

> Run an SEO deep dive on you, the five competitors,

John Mackenzie

> Then do a comparison analysis, nothing unusual in that, then drop an AI search engine assessment and a G, so engine optimization assessment, so you've got now three of them, not the one, now you've got three, then conduct something like what I do all the time when I'm speaking to my AI, then do something like a So I ask, what's the same, what's different, where's the white space, and what's the opportunity analysis?

Dr. Will Fisher

> Okay, so like a SWOT analysis? Yeah, right, but no, because a SWOT is really about you, but this is doing a SWOT for Against the other folks.

> Yeah, a comparable SWOT analysis. Right. And if you ran that comparable SWOT analysis through the lens of SEO, AEO, and GEO, right?

> lot. Bye.

John Mackenzie

> Man, that's really interesting stuff right there. Okay, John, can I ask you a question? So for psychology, I'm trying to think what I want to do, which I kind of like your idea about, you know, looking at maybe the top 20, the top 50 of folks, what people are doing, and then seeing if there's not something within that I could put together.

> So when you say psychology, what do you explicitly mean? I'm not exactly sure yet, but my background is in psychology, and so to figure out a niche within that.

> Okay, type of psychology are you involved with?

Dr. Will Fisher

> Like clinical or, yeah, I'll go the clinical psychology route. So more, but it could be like, it could be like dating, it could be like, you know.

> I would have fun with it. I'd play with it. I would run a, so what I'd do is I'd

John Mackenzie

> So a big five-factor, I'd run a big five-factor ocean with a hexam, 16 personalities, and a analysis. psychological tests, by the way, guys.

> What's that, sorry? I said I was interpreting for them. These are all psychological tests. Yeah, they're all psychological tests, right?

> So I would run a synthesis of all of them in the one pane of glass, right?

Dr. Will Fisher

> Okay. I would then do some general testing around ADHD. Yeah, and that's actually my dissertation.

John Mackenzie

> Oh, there you go. So I'd run over the top of the synthesis, ADHD. Yeah. But I could do, like, Enneagram.

> Spectrum. I could do, like you're saying, Spectrum, like some sort of Spectrum test about how, you know, Asperger's are you?

> Or- . And then general executive reasoning, because what I found that, when I went down that pathway, found that I've got high-functioning Asperger's, I've got ADHD, and I've got general executive reasoning, that's not reasoning, a dysfunction, executive dysfunction.

Dr. Will Fisher

> If you've got a low blood flow in your prefrontal cortex, that's where all your executive functioning happens.

John Mackenzie

> Then what I did was I mapped all that. I mapped all that in an Excel document. Now, what you could do is you could actually lift all of that across those different verticals, drop the baseline typical type of tests, drop a synthesis over the top of it.

> Now, being a psychologist with a dissertation and you're doctor, man, you're the perfect person to do this because you've got...

> You've got the credibility in it. That's what I'd be doing right there. Then I would drop things like the view.

Dr. Will Fisher

> I would drop different perspectives and views across the top, like Semantica, Archify, the God's Eye View. Because when you look at something God's Eye View, you're not looking at from a global perspective.

> You're actually looking at from a connectivity perspective, like graph nodes. Yeah, which a lot of ASD people are visual, and so it would really help them, actually.

> Absolutely, right. And then what you can do is as you get to the node, the node expands so that node expands the characteristics that then has edges to other nodes.

> That's what I'd be doing because, man, I don't – what I see at the moment with the stuff that we've just spoken about right now, no one globally has done anything like that.

John Mackenzie

> Yeah, I've just been looking for the idea, that's why I'm hanging out with you fellows that are smarter than me, at least on the tech side.

> But yeah, good stuff. Well, I'll have to start this and then run it by you later. We'll see what's going progress.

> You've got Claude Code, right? Oh, yeah, that's, that's, well, I mainly, I mainly have used just Google Sheets, though, and so it recommended I don't need Claude Code yet.

> But I've been asking it, like, do I need Claude Code? And they said, well, maybe if you're on your own machine, or your own database or something, that that may.

> So have you got a chat, you can chat GPT? Yeah, I actually stopped that one, but I can go back.

> usually use complexity and I was using three, but.

Dr. Will Fisher

> Whatever your flavor is, right? Yeah, they're all the same, and perplexity, you use Claude or any of them. So you've got.

> Your chat flavour. Use your chat flavour. Spit out a deep idea based on your body of knowledge and stuff that we just spoke about.

> Get that really strong.

John Mackenzie

> Get it to develop a prompt with a synthesis layer. Then once you've got that, if you just then ask it to write a prompt for like, so you're going to want a prompt around, you've got to, you've got to source the information from the, from the person.

Dr. Will Fisher

> So you need various interfaces that you can source that.

John Mackenzie

> Then you want to capture the data and then you want to present the data and the present, the data is going to be your UX UI.

> And then you're going to have like these different, you want to drop different perspectives across the top on the vertical, right?

> So the vertical is going to be. You just sort of lost me in that part. I think I get it now.

> You're talking about the drop the different perspectives on the X to the Y. It's just depending on – I think I get it now.

> Yeah, so the vertical is going to be the big five. Yeah, yeah. So the vertical is going to be the big five factor.

> It's going to be the 16 personalities, the good one, not the bad one. You're going to want to put the hex on, and then you're going to want to do ADHD, Asperger's, executive dysfunction.

> I'd be doing all those verticals because that's going to give you synthesis. Across – It should be some traffic too.

> Oh, man, it's going to get you the traffic. That's the ones that people are talking about. mean – Yeah, yeah, of course, right.

> Then across the top, that's when you're going to put your presentation verticals across the top, the views. And that's when you're going to drop something like God's Eye View.

> You're going to say, use God's Eye View. Use Archify. Use Semantica. Use that as inspiration to create You three or four different user perspectives, different interface views in a tabbed menu structure that all you need to do is work out what's the interface of the user, of how the AI or how the platform is going to interface with the user to extract it.

Rick Rodriguez

> Figure that last part, and that could be like this Yeah, need to ask you that later.

Jobi Armstrong

> Yeah, yeah, that could be a questionnaire, but you could make that a verbal questionnaire, right? So then, because with voice and questionnaire, like they would just speak the answers versus actually having to type them in?

> Or do you have a checkbox? Yeah, yeah, I'd do both. But then what I'd also do is run a behavioural analysis across the verbal, because you'll pick up some other indicators that the verbal will give you indicators to.

> Yeah, that's what I was thinking about too. Yeah. That's what I'd be doing. Yeah. Fascinating. Okay. Now you've, uh, I have to study for my exam as soon as I get this exam done, but I'm going to kick around this and start it.

> Yeah. Rock and roll. Yeah. Very cool. Very cool. Sweet. Well, I was going to show discord to you, Rick.

Dr. Will Fisher

> Are you, you've got this. I'm sorry. Say that again. You were kind of garbled discord. You got it figured out.

> Or do you want to show, you want me to show you a little example of what you can do to set how to set some stuff up?

> yeah, please, please do. Okay.

Jobi Armstrong

> So. Here's a pretty good example, like, you can come over here, make sure I'm showing the thing here, so here's your channel, right?

> We have just the general channel in here. Since you're the channel admin, you should be able to put a bunch of different channels in here, right?

> Do you know how to do that? I do. Okay, cool. So news research is a good one, so like, they have announcements, so you're probably going to want to do an announcements channel.

Dr. Will Fisher

> They have a page for developers.

Jobi Armstrong

> They have chat, LLMs, off-topic, interesting links, that's what we were talking about earlier, just, and you can also come in here, literally, like, right now, there's a, there's two voice chats going on, and there's this many people right now in a, in a voice chat, talking, just like we are, but inside of Discord, so like, and this is in news?

> Yeah.

Dr. Will Fisher

> So, like, if.

Rick Rodriguez

> we want to take things offline and get off of Google Meet, we can jump over into the guild and start talking over there for people that don't want to be on the Google Meet or whatever, know what I mean, like, or not recorded a little bit less of a formal environment over here, I suppose.

Patrick Thomas

> Botchchannel, that's what I was checking out earlier, like you already have, it looks like you have your Botchchannel, like you have Nova as the Botchch, so that's cool.

Jobi Armstrong

> Botchannel, I don't know, I think that theirs is set up pretty good, I guess they have their terms, onboarding data sets, stuff like that, so support threads, community project showcase, plug-ins and skills, so join their community and you can get a good idea of what you can set yours up like, kind of mimic it a little bit.

> Botchannel, yeah, somehow they got into one of my

Patrick Thomas

> I think it's in general. you go to general, you'll see noose at the top, or is it in the ask?

Dr. Will Fisher

> Is it in there? You scroll up. Yeah, right there.

Patrick Thomas

> You just passed it. don't know. Down, down, down. Right there. So you're in a different community as well. Is that what you were showing us, Jobi?

> I kind of looked away for a minute. Yeah, that was Noose Research, which is the owner of Hermes.

Jobi Armstrong

> Okay. You're in that community? Yeah, and then I'm also in, like, OMP.

Dr. Will Fisher

> I got, I'm in PIE. I'm also in BridgeMind, AMI, Noose Research.

Jobi Armstrong

> This is a motor sports community. High-portage electric bikes, water plowder, and scooter hacking. Scooter hacking. So how do you take their, like, their channels and bring them into?

> Is that what you're saying, I can bring their channels into my server, or no? No, I'm just showing you an idea of how to structure your channel, how to set it up with certain announcements, because you don't want everything to go into a general, you don't want everything living in general, it's going to be too hard to search for it, so you want to create multiple channels so you can basically parse through the data that's going inside of your channel, basically.

Dr. Will Fisher

> Okay. your base. All right.

Jobi Armstrong

> If that makes sense. Yeah, definitely. Yeah. Cool. I will look at that. This one's cool, man. Anyway. Yeah, I'm just, I'm still, just that much know about it.

> Yeah. All right. Well, I will show off a project that I'm building next time. I'm, like I said, I've been going through.

Dr. Will Fisher

> What is it? you much. much. Is this built with Astra? I'm building with Astra. I guess I could show it right now.

> It's very similar.

Jobi Armstrong

> Well, I started with the unified. Here, I'll just pull it up. I started with the unified LLM router and it looks a lot like what John has actually.

> But so I had basically what I did is I asked Astra to look at my unified LLM router project, my Nexus or AgentOS project.

> And then I put a few other GitHub repos into this and I asked it to redesign it for a workspace agent command hub, right?

> So it's very, it's kind of interesting because it's a very similar layout to what John has. And I don't know.

> It's just kind of funny. So anyway, but up here you can go and you can have different workspaces. So this might her.

> It actually has the project that I'm working in it right now, which is this Luna, I call it Luna, the Luna Hub, so it shows what's going on in here.

> And I created a graph view. You can see how many tokens and how long the project has been being worked on, the current stage, which is in the design stage.

> What top of graph is that? It's what? It's very nice, very . I actually went in and did some research with ChatGPT and asked it to spit out 10 different neural LLM graphs, different styles.

> And then I actually picked two of them and combined the two of them. And I said, combine this one and let me actually go into my actual chat here that I did.

> Where did it go? Unified LLM, LLM graphs. Oops. That is super . Thank you. So I went in here and like I said, I said, give me an example of different kinds of machine learning graphs for visual design and cohesiveness.

> It spit this out and I actually combined number one neural network with number two and by the embedding clusters.

John Mackenzie

> And it came up so they combined the two and it came up with this and it's a neural cluster is what it's called.

> And so you can actually come over in here and and it tracks it and it comes down in here and it'll change it right here.

> shows you it. Right. So there's that view and there's also the information just a different style of if in case people are vision different visually learner like learning, you know, so.

> So, but I love that as well. Yeah, I like this.

Jobi Armstrong

> I neural graph a lot because it just looks cool and it feels good, too, right? And then there's kind of a menu down here where it shows you what's going on, recorded bridge, selected relationship, inferred, and planned.

John Mackenzie

> Would you be happy to ask your agent to just write the code of those two graph views and that instruction below it, right?

> So, and then just drop it. So, because, man, that graph view that you've got with both of them, actually, are so , right?

> They are, like, I'd never thought about going and doing that, you know, what you just did. That is so good.

> Thank you. Appreciate that. Of course. I'm happy to, happy to. I'll be happy to do the same with whatever I'm just thinking of it, with my God's eye view, the things that I'm spitting out at the moment, because what you'll end up doing is, you'll end up doing something else with it, you know, because it'll be different, different data, different this, different that.

> It's just a block. That's all it ends up becoming. And then what, you know, your AI is going to interpret the block how it wants to interpret the block based on your data.

> But to get to, obviously, that's the whole point of having an open source Git, because you see something that's so good.

> You rip the open source Git, then you give that to your AI, and it's like 90% further down the track.

> But that's what I see with what that there, what that is there. You know what you should do, Jobi?

> If I was you, because that is so sick.

Jobi Armstrong

> I would have like five or 10, I'd create.

John Mackenzie

> Five or ten others just for that, I'd probably drop an open source, right, on Git and then get people to see it because I imagine, you know that the YouTube that I just showed you with those two guys, with that one guy, this is the type of thing that I think people would see, they'd love, they'd actually connect to it, they'd star, and they would fork and download.

> And if that's something that you've got interest in for doing that sort of thing, I don't, it's only a block of, you know, like a graph, so it wouldn't be that hard to actually build out like five different or ten different blocks of graph, but anyway, man, that's so , well done.

> Thank you, I appreciate that. I like that idea too, I'm obviously taking notes when you're talking about this, so that's a good idea.

> I I'm telling you that that's why.

Jobi Armstrong

> It's of the best graphs that I've seen for a long, long time, and because it's that , you know, look, it'll help blow up your brain, depending on what you want to do, right?

Dr. Will Fisher

> It depends on where you see you are now, what you want.

Jobi Armstrong

> But, you know, for me, I'm not in the market of trying to make money out of a block, you know, a graph block.

John Mackenzie

> You're probably not either. So you, it wouldn't take much to, like, I could probably do the same with the merge of some of the blocks that I'm starting to develop at the moment, but, oh, man, that looks .

Jobi Armstrong

> I really like how that, yeah, I mean, it looks like it's thinking, man.

John Mackenzie

> That's just cool. It reminds me of the neural network of the brain. yeah, yeah. And how it links. Synapses.

> There's a few connectors, and I- When I designed this, I actually hooked up into the Higgsfield plug-in, and I ran out of credits because I was on the free trial.

> Higgsfield is insanely expensive, but Higgsfield helped me design this because their platform is pretty amazing because they have all the… Wait, wait, wait, wait, wait, wait, wait, wait, wait, wait, wait.

> That's so sick. Yeah. I never thought of doing something like that either. So you designed… So did that design the animation or the full graphic as a base, and then you ported that into your code platform?

> I did. I brought Higgsfield in as a plug-in, and I used the Higgsfield plug-in to help me design the draft to make it look more interactive.

> Oh, man, that is so sick. Yeah.

Jobi Armstrong

> You know, have you tapped, have you tapped, sorry for interrupting your presentation, Jobi, but this is so good, mate.

John Mackenzie

> Have you tapped the… Um, what Selena said the other day, Lenny's product pass. No, you got a link. Does it have Higgsfield in it?

> It does have Higgsfield in it. It does have Higgsfield in it, I thought. Can you put a link to that Higgsfield?

> Hey, I'll have it in the chat. I'll drop this in the chat in a second. I'm just trying to find the products that's in here.

> Um, because as soon as you said Higgsfield, um, I had, uh, which products are in it? so you get, so you got $200.

> Yes. Anyway, continue showing. you do get Higgsfield. One year, free Higgsfield pro, $348. You get that as part of this package.

> What is this? Lenny, what? Are you dropping it? I'm dropping it right now. One sec. Okay. There you go.

> Thank you, Selena. I don't know if she's on at the moment, but, um, we had a good chat about this after everyone wound down last.

> No, she's not in right now. She was in there this morning.

Patrick Thomas

> Yeah, yeah, yeah. So the best thing that we have going on is people sharing the best stuff about saving money, making money, you know, what you've just done here, the idea that you got, how you did it.

> Man, what you, and now Hicksfield, right?

John Mackenzie

> Because if you spend 200 bucks, and it's on the $200 account, it's not even on the big one, right?

Patrick Thomas

> So on the $200 account, you get one-year free cursor. So that's the $20 cursor account. You get Hicksfield for one year, for 348.

> You get lovable repli for a little bit, both for one year as well.

John Mackenzie

> Because what, you can just tap some of the, and Superbase, right, for one year, Superbase pro credits.

Patrick Thomas

> But for me, I use most of those, and you get 11 labs for one year.

John Mackenzie

> The $264 obviously divided by 12, and then – so what you'll find for this $200, Jobi, you'll now get hits filled that you can tap Fathom more because you've got it for a whole – for $200, you get all of those things, maybe $1,000 for $2,000 worth of credits, right?

> I've got a question. Does this fall into the category of when you and I were talking about when I was going to sign up for Claude Code and I was going to get it for – if I bought the year package for $5 and $4.59 or whatever it was, and you go, yeah, don't do that because they can – what's the term I'm looking for?

> They can throttle your account. Is this the same kind of situation or is it just like getting a pull, like if you were to go out and buy all those things?

> No, the way I see this is And I could be very wrong, but the way I see, what they're doing is discounting heavily on an account that they can do whatever they want with.

> So they're the main, they're doing it themselves, you buy it direct and they do whatever. What this here is, this is marketing.

> So they're going to someone and selling it at such a discount to massively increase their user headcount. So this will help them with their, their angel, their venture capital, their seed rounds.

> They're discounting across the top, but they're getting headcount and it's not well known in the mainstream. So they're not, they're not dropping the discount and they're not dropping their pants, their price in the, in the, in the marketplace.

> But what they're doing is giving away behind the scenes to increase user, so that, so. can do it. And if you have a look at it, the cursor, it's like 12 months at $240.

> How much is the cheapest cursor account? $20. So you're getting the $20 account for 12 months.

Jobi Armstrong

> If you look at Lovable, similar type of thing. Higgsfield, what I see at the moment with their price points is they're just giving away their cheapest entry model, right, to an aggregator essentially to get headcount use, right?

> And for me, I saw Higgsfield on there.

Patrick Thomas

> I thought, to be honest, Jobi, I thought, oh, no big deal. Superbase, absolutely. Cursor, absolutely. Right. Replit and Lovable, just going to create more challenges in my stack.

Jobi Armstrong

> So it's not worth it, right? about it's It's got think But that's a Hicksfield, based on what I've just seen, what you did, it's like, hmm.

> Yeah. Hicksfield is a really convenient connector if you're trying to do elaborate designs as well. If you really want to put out some really nice designs, Hicksfield, the Hicksfield connector or the MCP, it's kind of funny.

> ChatGPT Codex has plug-ins, but obviously Code, sorry, Claude has MCP connections. It's basically the same thing, but set up just a little bit differently.

> I've got ChatGPT doing a deep dive on that site, too. Nice. And what's the real deal on that? Tell me what the gotchas are, so I'll see what it comes back with.

> I'll just speed run through this really quick. So down here at Connections, we have your models, we have your agent apps, so you have your Harmony's, COD code, MCP servers, and then we have files and machines.

> So... Cloud VPS and whatnot. So over here you have a blown up view of it, sync, the computer's sync, the VPS is sync, the cloud runner, whatever, it's ready.

John Mackenzie

> Down here you have a chatbot.

Jobi Armstrong

> Obviously it's not ported yet, but you can, you have the chatbot inside of here if you want to use it.

> You can add a machine up here. And then we can go, let's go back to, I also have a way to put terminal.

> Obviously the terminal's not ported. I'm going to use a WES term for this so I can use terminal directly inside of this workspace.

> Files and artifacts, you can go back here. This is where all your files are going to live for this project.

> So your PDFs and whatnot, artifacts as well. We have a skills vault that we can obviously, whatever, it's kind of the name says it's all, right?

> What I like about this is the memory. What I didn't really tell to do is to build this client.

> Client. And I was like, I thought this was kind of cool. If you want to, if you actually have a client, you could literally use your, your agent OS system here and have, and send, I don't, I don't have it set up yet, but you should be able to send this out to your client so they can work with their, your, you can work on their project with them inside of your workspace.

John Mackenzie

> Right.

Jobi Armstrong

> So, um, that's something that, yeah. Um, so I have it, you know, the workspaces are separated. So like I said, personal client collaboration and then like DHC, which is my construction company.

John Mackenzie

> So I have my contractor compliance, uh, project over here and that's how it's broken up. It's broken up into projects on the side here.

Patrick Thomas

> So obviously when more projects come, it'll come down to here and we have our, we have our settings page, our members, who is, who's all in here as a member, if they're active or not, access and usage.

> Um, so yeah, I mean, that's kind of what I got. There's a lot of things I still need to port.

> Okay. There's a lot of things I need to make sure they're going to work properly, but that's the overview of what I've been trying, and the vision finally kind of came alive, because this is what I've been wanting since the beginning, but I haven't just been able to put it together, and it's finally starting to come together.

> Man, that is so sick. Thanks, appreciate it. Well, lots of inspiration from everybody in here, you know, so, yeah, I appreciate everybody.

> Joshi, you're, oh, that is, that is the best page, that one there. Hey, check this out, you know, for my conversation, I just want to show you this real quick.

> had Brock Bill do this, and you're talking about calculators and all this kind of stuff. I went, and I gave Brock, and this is, this isn't a live page, but it's on my, like, my dev for the, for a wrap.

Jobi Armstrong

> Thank very much. very much. Thank Thank Thank you very Thank Thank Thank I told them to create a tools page, so this is a tools page, and it's a desk drawer for people writing bids, bid map quantities on the desk, scoping paper, and it's like you click on, like, I don't know, quantities, and their waste factor, it's like, put some calculators out here that people will use for the, for the, you know, contractors can use.

Patrick Thomas

> I don't know. How good is that?

John Mackenzie

> Yeah, it just did it.

Patrick Thomas

> Drywall, you know, I guess you could just change this, you could change this to like, I don't know, Wow.

John Mackenzie

> Four doors. I love this. I love this a lot.

Patrick Thomas

> I mean, this is kind of. Is that cool? It's very Oh, my that's so good. You just made this?

> Yeah, I had God, Bill, just make this based on our conversation. I said, yeah. I love this a lot.

> That is so sick. And I'm just, yeah. Yeah, that's awesome. Thank you for sharing that because that just gave me a bunch of ideas.

Jobi Armstrong

> That happens, dude. That happens when you get in here and start doing this stuff.

Patrick Thomas

> It's like, oh, my God, that's so cool. This is so good. Just sharing stuff with other great people is amazing.

> Right? Oh, my goodness, man. I'm on the Google page. Oh, and I haven't spun this up yet.

Jobi Armstrong

> I'll just show you one more thing. Remember that thing I tried? So I had it. This is on my local server, so it's not on the site.

Patrick Thomas

> But if I go to what's next. I told her what's next, this is Rapid Field, this is the thing I sent you, and this has the new, this is the thing that you can install on your iPhone or your Android and take in and take, you click on this, it shows you, you know, you take pictures and then put in the measurements, whatever, markup and all that.

> Basically, you set your job up and then you export it to an XML and then you import the XML right into the desktop program.

John Mackenzie

> And then I told her that other rapid estimator updates, a website refresh, AI assist pilot, we're going to put that in, you know, just stuff like that.

> But that's the only thing I had to do. Amazing. So, yeah, I wanted, because the other thing I told the AI, said, go out to my website, because I need some more stuff to sell.

Patrick Thomas

> Go look at my website and look at my competitor's website and what, what, what else can I offer?

John Mackenzie

> Go. Go. Thank you. To make more money, and it gave me like four or five different ideas that, you know, just add-ons that I can sell along with this product, so.

> So awesome. Unbelievable, unbelievable. Got to turn these ideas into cash, man, do that. And it does take a little bit of time to do it, but, you know, the stuff that's starting to drop from some of the guys, some of the people, it's just amazing.

> Oh, man. I think my brain is full for tonight. Oh. But I've got so many good ideas. Oh, yeah, Will.

> So, thank you all. I'm gonna go as well. You guys are killing me, but, man, Jobi, Patrick, everyone, thank you so much.

> It's just been such an awesome night. Yeah. Thanks, everybody. I had a good time, and I guess we'll see what's tomorrow.

> Thanks, everybody. We'll see you later. All right. See you at the next one. Take care. Take care. This is pure energy.

Enhanced

EnhancedFree

Capture any call's insights and key takeaways.

Sales

Unpack a prospect’s needs, challenges, and buying journey.

Sales - Sandler

Notes based on Sandler Selling System

Sales - SPICED

Notes based on the sales methodology by Winning by Design.

Sales - MEDDPICC

Notes based on the popular sales methodology.

Sales - BANT

Notes based on the popular sales methodology.

Customer Success

Experiences, challenges, goals, and Q&A.

Customer Success - REACH™

Notes based on an expansion framework by HelloCCO

Candidate Interview

Delve into a candidate’s experience, goals, and responses.

Demo

Showcased journeys and impact.

One-on-One

Updates, priorities, support signals, and discussion.

Project Kick-Off

Vision, targets, and resources.

Project Update

Breakdown each task’s status, discussion, and next steps.

Q&A

Recap questions with answers.

Retrospective

Capture processes to start, stop, and continue.

Stand Up

Track daily progress, tasks, and obstacles.

🇺🇸EN

🇺🇸English

🇪🇸Spanish

🇵🇹Portuguese

🇩🇪German

🇫🇷French

🇮🇹Italian

🇳🇱Dutch

Copy Summary
![](https://static.fathom.video/3ba757e2c93a13e99490fcb3571eb12849397a31/components/build/assets/app-icons/docs.svg)

## Meeting Purpose

To share AI-driven projects, discuss technical challenges, and brainstorm new ideas.

## Key Takeaways

- **GrokBot VPS Access:** The GrokBot VPS is a locked sandbox, not a general-purpose machine. SSH access is possible via Tailscale, but external control from other LLMs (e.g., Codex) is unreliable, as it often defaults to previously configured VPS connections.
- **AI-Driven Project Management:** John demoed a stock trading simulator built in 6.5 hours and an internal dashboard to manage his 17 pre-prod GitHub commits. Jobi shared a "Luna Hub" agent OS with a stunning, interactive "neural cluster" graph UI.
- **Monetization Strategies:** A key strategy emerged: create a central hub for a niche (e.g., design assets, psychology tools) by aggregating open-source resources. Monetize with AdSense, automated SEO blogs, and custom calculators.
- **Cost-Saving Deals:** The "Lenny's product pass" was highlighted as a high-value bundle, offering a year of Higgsfield Pro ($348 value) plus other tools for a $200 one-time fee.

## Topics

### GrokBot VPS Access & Limitations

- **Problem:** Jobi asked how to use the GrokBot VPS outside the GrokBot interface.
- **Clarification:** The VPS is a locked sandbox, not a general-purpose machine. It lacks a public IP and direct SSH access.
- **Solution:** SSH access is possible via Tailscale. Patrick shared instructions for connecting to `tailscale ssh grok.box`.
- **Experiment:** John tested running small LLMs (e.g., Llama 3.1 8B) on the VPS.
  - **Result:** Codex failed to use the GrokBot VPS, defaulting instead to a previously configured Hostinger VPS. This suggests unreliable external control from other LLMs.
- **Patrick's VPS Utilities:**
  - **Disaster Recovery:** A script to restore the VPS environment (e.g., installed browsers) after a reboot.
  - **`lag` Command:** A one-word command to kill dead tabs and processes, instantly improving performance without a reboot.

### AI-Driven Project Management & Development

- **John's Projects:**
  - **Stock Trading Simulator:** Built in 6.5 hours using Codex.
    - **Function:** A paper-trading simulator for ASX, LSE, and NYSE.
    - **Goal:** Test multiple AI-researched trading methods simultaneously.
    - **Future:** Use historical data and ML to identify market patterns.
  - **Internal Project Dashboard:** A "single pane of glass" to manage all projects.
    - **Challenge:** 17 pre-prod GitHub commits need merging to `main` without conflicts.
    - **Solution:** An AI agent will analyze commits and create a safe merge strategy.
  - **Intelligence Gathering:**
    - **Process:** Scrapes GitHub repos from the top 200 AI token users.
    - **Rationale:** To identify and "rebuild better" the best ideas from prolific AI developers, avoiding attribution or forks.
- **Jobi's "Luna Hub" Agent OS:**
  - **Function:** A personal agent OS for project management.
  - **UI:** Features a stunning, interactive "neural cluster" graph view.
  - **Tech Stack:** Designed by combining two ChatGPT-generated graph styles. The animation was refined using the Higgsfield plugin.
- **Patrick's Tools Page:**
  - **Function:** A contractor tools page with embedded calculators for bids and quantities.
  - **Creation:** Built by GrokBot during the meeting, demonstrating rapid AI-driven development.

### Monetization & Business Strategy

- **Core Strategy:** Create a central hub for a niche by aggregating open-source resources.
- **Monetization Pillars:**
  - **AdSense:** Generate revenue from site traffic.
  - **Automated Content:** Use an AI agent to create SEO-optimized blogs (e.g., on fonts, color theory) to drive organic growth.
  - **Custom Calculators:** Build free, valuable tools that attract users and capture search traffic.
- **Example Application (Dr. Will Fisher):**
  - **Concept:** An AI-powered psychology synthesis platform.
  - **Function:** Combines results from multiple tests (Big Five, 16 Personalities, ADHD) to create a unified profile.
  - **UI:** Uses graph visualizations (inspired by God's Eye View) to show connections between traits, which is highly effective for visual learners.
  - **Data Input:** A verbal questionnaire would allow for behavioral analysis of the user's responses.

### Discord Server Setup

- **Goal:** Use Discord as a persistent community hub between Google Meets.
- **Recommendation (Jobi):** Create dedicated channels for specific topics (e.g., `announcements`, `interesting-links`, `bot-channel`) to keep discussions organized and searchable.

## Next Steps

- **Rick:**
  - Restructure the Discord server with dedicated channels.
- **Patrick:**
  - Implement the `lag` command and disaster recovery script in the GrokBot VPS.
- **Jobi:**
  - Share the code for the "neural cluster" graph view.
  - Explore creating an open-source library of graph components.
- **Dr. Will Fisher:**
  - Begin planning the AI-powered psychology synthesis platform.
- **John:**
  - Continue developing the stock trading simulator and internal project dashboard.
- **All:**
  - Evaluate the "Lenny's product pass" for its cost-saving benefits on Higgsfield and other tools.

![](https://static.fathom.video/3ba757e2c93a13e99490fcb3571eb12849397a31/components/build/assets/fathom.svg)

Hi, what can I tell you about this meeting?

- Detail all timelines discussed
- Describe the key stakeholders?
- Who else should we speak to?
- What would help make progress?

Impromptu Google Meet Meeting

Sep 9, 2026

Share

#### Your Questions

- “Does anybody know what this origin is?”
- “Or are you just literally using it inside the cursor app? How are you?”
- “John, where do you get the users from? How do you know that they're top token users and stuff? How do you?”
- “Does that make sense?”
- “Can't GrokBot reach out to the browser and control it? I was actually just trying to, I was just using it in there to try and create that Discord bot.”
- “What is God's EyeView?”
- “So is that where the data is flowing to and from all those different?”

#### Their Questions

- “How are you doing, Rick?”
- “Did you get the time change again?”
- “That was the, what is this?”
- “Who has something they would like to share? Oh, Patrick, were you saying that you were working on something that you were going to do something for tonight?”
- “Yeah, I'm asking, so basically you're saying how do I open up the SSH?”
- “What platform do you use to trade, Patrick?”
- “I know Slack's a Linux OS too, isn't it?”
- “Yeah, but with the GrokBot, if you're using the VPS, isn't it still, by using that VPS, isn't it still using some kind of usage through Grok? Ah, see, I've solved that.”
- “So are you talking in Grok's VPS?”
- “Is there a reason you did that?”

![](<Base64-Image-Removed>)

# Network Error

We detected an error while loading the requested content.

Reload Page [Contact Support](mailto:help@fathom.video?subject=Network%20error%20while%20using%20Fathom)