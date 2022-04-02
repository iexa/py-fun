{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "# https://stackoverflow.com/questions/36786722/how-to-display-full-output-in-jupyter-not-only-last-result\n",
    "from IPython.core.interactiveshell import InteractiveShell\n",
    "InteractiveShell.ast_node_interactivity = 'all'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import collections\n",
    "\n",
    "Card = collections.namedtuple('Card', 'rank suit')\n",
    "\n",
    "class FrenchDeck:\n",
    "    ranks = [str(n) for n in range(2,11)] + list('JQKA')\n",
    "    suits = 'spades diamonds clubs hearts'.split()\n",
    "\n",
    "    def __init__(self):\n",
    "        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]\n",
    "\n",
    "    def __len__(self):\n",
    "        return len(self._cards)\n",
    "\n",
    "    def __getitem__(self, pos):\n",
    "        return self._cards[pos]\n",
    "\n",
    "\n",
    "deck = FrenchDeck()\n",
    "len(deck)\n",
    "deck[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Card(rank='J', suit='hearts')"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "text/plain": [
       "[Card(rank='2', suit='diamonds'),\n",
       " Card(rank='3', suit='diamonds'),\n",
       " Card(rank='4', suit='diamonds')]"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "text/plain": [
       "9"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from random import choice\n",
    "\n",
    "choice(deck)\n",
    "deck[13:16]\n",
    "FrenchDeck.ranks.index('J')"
   ]
  }
 ],
 "metadata": {
  "interpreter": {
   "hash": "65288dce7ba102a790c7c62afa0efb87e36ee2af5f5100d40cd14cc6b0a85477"
  },
  "kernelspec": {
   "display_name": "Python 3.8.10 64-bit",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
