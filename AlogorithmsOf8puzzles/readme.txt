This readme is about the IDA* algorithm.
The main idea of my algorithm is from wiki, which psudocode is this:

 ===============================================
 node              current node
 g                 the cost to reach current node
 f                 estimated cost of the cheapest path (root..node..goal)
 h(node)           estimated cost of the cheapest path (node..goal)
 cost(node, succ)  path cost function
 is_goal(node)     goal test
 successors(node)  node expanding function

 procedure ida_star(root, cost(), is_goal(), h())
   bound := h(root)
   loop
     t := search(root, 0, bound)
     if t = FOUND then return FOUND
     if t = ∞ then return NOT_FOUND
     bound := t
   end loop
 end procedure

 function search(node, g, bound)
   f := g + h(node)
   if f > bound then return f
   if is_goal(node) then return FOUND
   min := ∞
   for succ in successors(node) do
     t := search(succ, g + cost(node, succ), bound)
     if t = FOUND then return FOUND
     if t < min then min := t
   end for
   return min
 end function
 ===============================================

You can find the detailed description in the code comments.

I got to know that it's really important to find a good evaluation function in the A* and IDA* algorithms!






