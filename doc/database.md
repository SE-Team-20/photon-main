# Method guide for src/database.py

[quick link](../src/database.py)

## 1. APIs

<table>
<thread>
 <tr>
  <th>method name</th>
  <th>purpose</th>
  <th>input</th>
  <th>output</th>
 </tr>
</thread>
<tr>
 <td>close()</td>
 <td>close the database</td>
 <td></td>
 <td></td>
</tr>
<tr>
 <td>set_player()</td>
 <td>assign a codename to the specific cell</td>
 <td>player ID, team ID, codename</td>
 <td>True/False</td>
</tr>
<tr>
 <td>update_score()</td>
 <td>applies a score change to a specific player</td>
 <td>difference, player ID, team ID</td>
 <td>True/False</td>
</tr>
<tr>
 <td>get_leaderboard()</td>
 <td>gets an array representing a leaderboard of one team in non-decreasing order</td>
 <td>team ID</td>
 <td>tuples of {rank, codename, score}</td>
</tr>
<tr>
 <td>get_player_info()</td>
 <td>gets a player information from the equipment ID</td>
 <td>equipment ID</td>
 <td>a pair of {team ID, player ID}</td>
</tr>
<tr>
 <td>assign_equipment()</td>
 <td>associate an equipment ID to a player ID (no duplication)</td>
 <td>player ID, team ID, equipment ID</td>
 <td>True/False</td>
</tr>
<tr>
 <td>free_equipment()</td>
 <td>free an equipment from any players</td>
 <td>equipment ID</td>
 <td>True/False</td>
</tr>
<tr>
 <td>clear_equips()</td>
 <td>free every equipment</td>
 <td></td>
 <td>True/False</td>
</tr>
<tr>
 <td>clear_players()</td>
 <td>re-initialize every player info</td>
 <td></td>
 <td>True/False</td>
</tr>

</table>

## 2. Relational database structure
1. player ID x team ID - codename - score
2. equip ID - player ID x team ID