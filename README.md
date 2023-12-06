This was the final code used for the Inbox Marketer 4910 project in F17.

I found after much training and flipping things around, that there was an
issue with either the dataset or the actual methodology approach, which will
be covered later.

When reviewing the dataset and attempting to parse it, six different cases
were come across as trends. These included:
1) ##TAG## string							
2) ##TAG## string ##TAG##					
3) ##TAG##%								
4) test_##TAG##_##TAG##					
5) ##TAG## string ##TAG TAG##				
6) Normal string with no special cases

The tags were identified to be important to inbox marketer, as it was their
form of personalizing an email subject line. By doing this, it is hoped
that more customers would open and click things inside the email, thus
increasing user interactivity.

Once the data was parsed, it was saved to a file called "preprocessed.txt",
which follows the style:
          subject:::openRate:::clickRate
The reason the three colons were used was to allow ease of separating the
data based on a token, ie: the three colons.
The data should then be shuffled, and split into the desired training and
testing ratios.
After splitting, the neural network can be trained, and tested afterwards.

The current execution of this program should follow this order:

1) python main.py
2) 1 - Preprocess the CSV file
3) 2 - Generate the dictionary
4) 5 - Shuffle the dataset
5) 3 - Train the Neural Network
6) 6 - Quit
7) python main.py
8) 4 - Test the Neural Network

Currently there is a bug in the system that does not let the Neural Network to
be trained then tested in the same instance of the program, so exiting and
restarting is required to do this process.
Additionally, the program can't test two times in a row, ie: testing and testing
again right afterwards.

Sadly, while testing, it was discovered that the maximum accuracy this model
could produce was around 10-20% accuracy. This could be due to many things:
1) The dataset not being set up properly
2) The wrong variables are being looked at
3) The specific type of Neural Network used in this approach could be wrong
4) There is a logic error that I couldn't find

In further explanation of these:
1) Upon creating the dictionary initially, it was discovered that the most
   frequent line used was "Hey, you left something in your cart". Throughout
   the dataset, a majority of the lines were repeated, so it wasn't sure if
   the dataset could be modelled properly. I suggested at the end of the
   semester to look at aggregating the repeated subject lines and their specific
   rates, and maybe using that as a better indicator of the importance of the
   words used in the subject lines, instead of a dataset where ~20,000 of the
   ~600,000 subject lines were "Hey, you left something in your cart"
2) The dataset has a lot of variables. Many of them pertain to the time an
   email campaign went out, and when it was finished being delivered. I believe
   it may be important to look at how the time of day an email was sent, since
   it could be a better indication of user interaction.
3) The specific approach I used was a Feed-Forward Neural Network. I used this
   since I've worked with them before, and due to much of my time being spent
   on analyzing and processing the data. Upon further research of Neural Networks,
   I believe it may be interesting to look into either a Deep Belief Network or
   a Recurrent Neural Network, as they are very strong at Natural Language
   Processing, due to the ability to store "memories".
4) Obviously I'm not perfect, so I could have easily done something wrong with
   my code that I didn't catch.


Should you have any further questions about the project or my findings, please
feel free to email me at houlding.patrick@gmail.com and I would gladly try my best
to help out! :)
