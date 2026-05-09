### Polarizer Tuple Calculator

This Python project may be used as a calculator for sums of products of powers of polarizers in tuple notation as introduced in my bachelor's thesis.

### Requirements

As we use N as a parameter, one has to load the `simpy` module in one's interpreter in order to run the script. 
* **Python:** 3.13
* **Sympy:** 1.14.0
* **mpmath:** 1.3.0

### Format

A sum of tuples of the same length (if the length differs one has to simply fill up the shorter tuples with zeroes) is a list, where the first entry
specifies the length of the tuples, the second a global factor and every additional entry a list consisting of a tuple (again a list) and a factor specific to this tuple.

`[length of tuples, global factor, [tuple1, coefficient1], [tuple2, coefficient2], ...]`

### Key Methods

* `tupsumsimplify`: Takes a sum of tuples and simplifies it, such that no tuple shows up more than once and tuples with coefficient zero are omitted.
* `add`: Takes two sums of tuples and adds them returning the simplfied result. The sums of tuples themselves are not manipulated.
* `multiplyandsimplify`: Takes two sums of tuples and multiplies them returning the simplified result. The sums of tuples themselves are not manipulated.
* `njm`: Given an up-down-tableau of length n. Call c its refined content, J the NJM operator of its predecessor tableau and A a list containing the refined contents of all other boxes that could have been added or removed from the predecessor tableau to obtain an up-down-tableau. This method takes J, c, A and n and returns the NJM operator for this up-down-tableau as a sum of tuples.

### Contained Examples

Upon running the script njm is used to calculate the NJM operators up to n=4. Up to n=3 they are written into a .txt file called njm.txt as code that can be readily inserted into LaTex. It can be found in this repository. 
This code is used to display these operators up to n=3 in Appendix A of my bachelor's thesis. 
The way in which the NJM operators are labeled is explained also in Appendix A of my bachelor's thesis. 
