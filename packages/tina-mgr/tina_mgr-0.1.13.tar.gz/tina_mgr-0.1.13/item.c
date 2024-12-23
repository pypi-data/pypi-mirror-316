/*
 * tina - a personal information manager
 * SPDX-FileCopyrightText: 2001  Matt Kraai
 * SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#include "item.h"
#include "memory.h"

/* Return a unique identifier.  */
static char *
unique_identifier (void)
{
  char buf[256];
  size_t len;

  snprintf (buf, sizeof (buf), "<%lx.%x@", time (NULL), rand ());
  len = strlen (buf);
  gethostname (buf + len, sizeof (buf) - len - 1);
  strcat (buf, ">");

  return xstrdup (buf);
}

struct item *
item_new (void)
{
  struct item *it;

  it = xcalloc (1, sizeof (struct item));
  it->identifier = unique_identifier ();

  return it;
}

struct item *
item_new_with_description (const char *description)
{
  struct item *it;

  if (description == NULL)
    abort ();

  it = item_new ();
  it->description = xstrdup (description);

  return it;
}

struct item *
item_clone (struct item *it)
{
  struct item *newit;
  size_t i;

  newit = item_new_with_description (it->description);
  newit->categories = xmalloc (sizeof (char *) * it->ncategories);
  for (i = 0; i < it->ncategories; i++)
    newit->categories[i] = xstrdup (it->categories[i]);
  newit->ncategories = it->ncategories;

  return newit;
}

void
item_delete (struct item *it)
{
  size_t i;

  free (it->description);
  for (i = 0; i < it->ncategories; i++)
    free (it->categories[i]);
  free (it->categories);
  free (it);
}

void
item_identifier_set (struct item *it, const char *identifier)
{
  free (it->identifier);
  it->identifier = xstrdup (identifier);
}

void
item_description_set (struct item *it, const char *description)
{
  free (it->description);
  it->description = xstrdup (description);
}

void
item_category_add (struct item *it, const char *category)
{
  if (! item_category_member_p (it, category))
    {
      it->categories = xrealloc (it->categories,
				 sizeof (char *) * (it->ncategories + 1));
      it->categories[it->ncategories++] = xstrdup (category);
    }
}

void
item_category_remove (struct item *it, const char *category)
{
  /*
   * NB: keep this signed because of the decrement at the end.
   *   -- Peter Pentchev  2010/06/04
   */
  int i;

  for (i = 0; i < (int)it->ncategories; i++)
    if (strcmp (it->categories[i], category) == 0)
      {
	free (it->categories[i]);
	memmove (it->categories + i, it->categories + i + 1,
		 sizeof (char *) * (it->ncategories - i - 1));
	it->ncategories--;
	i--;
      }
}

int
item_category_member_p (struct item *it, const char *category)
{
  size_t i;

  for (i = 0; i < it->ncategories; i++)
    if (strcmp (it->categories[i], category) == 0)
      return 1;

  return 0;
}
