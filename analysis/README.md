# Modelling polymorphic FKs and performance implications

## Problem

During the work on #145, the question of the most suitable approach to modelling polymorphic references came up again.
In this case, the `conformity_check` table has an n:1 relation to the resource to be checked, which could be any of the
following concrete resources:

* Service (WMS, WFS, CSW)
* Layer
* Feature Type
* Service Metadata
* Layer Metadata
* Feature Type Metadata

![Resource types](drawio_mrmap_polymorphic_fks-intro.png)

## Test scenario

To solve this, several different approaches are possible, and in order to find the best approach (and also to get more
confident in using the Django ORM), I implemented them and analyzed their performance implications in a test scenario:

| WMS    | WFS    | CSW    | Layers  | Feature Types | Service Metadata | Layer Metadata | Feature Type Metadata | Dataset Metadata |
|--------|--------|--------|---------|---------------|------------------|----------------|-----------------------|------------------|
| 10,000 | 10,000 | 10,000 | 100,000 | 100,000       | 30,000           | 100,000        | 100,000               | 20,000           |

The number of conformity checks was 100,000.

I considered the optimization options and actual performance for the common case of rendering a list view
using [django-tables2](https://django-tables2.readthedocs.io/en/latest/):

* Rendering list view (with links to resources)
* Rendering list view (with links to resources *and* properties from resource table)

### Test 1: Rendering list view (with links to resources)

![List View with links to resources](list_view1.png)

This use case gives an indication whether it is possible to efficiently determine the linked table and render a URL to a
linked resource.

### Test 2: Rendering list view (with links to resources *and* property from resource table)

![List View with links to resources and property from resource table](list_view2.png)

This use case gives the indication whether it is possible to efficiently query attributes from the linked table when
querying a conformity check.

## Compared approaches

Five different approaches for modelling polymorphic references were compared:

* Django's generic FKs
* Sparse FKs
* Sparse FKs in lookup table
* Multi-table Inheritance
* django-polymorphic

### Django generic FKs

This approach uses
the [generic relation mechanism](https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/#generic-relations)
provided by Django. Note that column `resource_id` in the `conformity_check` table is not an actual database foreign
key, it's simply a column that can store the primary key values of the different resource tables. The `resource_type_id`
column acts as a discriminator that defines the table targeted by `resource_id`.

![Model using Django generic FKs](drawio_mrmap_polymorphic_fks-django-generic-fk.png)

### Sparse FKs

This approach uses separate foreign key columns for each type of resource. For each `conformity_check` row, only a
single fk column must have a value different from `NULL`.

![Model using sparse FKs](drawio_mrmap_polymorphic_fks-sparse-fks.png)

### Sparse FKs in lookup table

This approach is similar to the sparse FKs approach, but puts 1:1 FKs into an intermediate `resource` table that has a
1:n relation to `conformity_check`. This potentially allows reuse of the `resource` lookup table, so polymorphic
referencing of resources is possible from other tables as well.

![Model using sparse FKs in lookup table](drawio_mrmap_polymorphic_fks-sparse-fks-in-lookup-table.png)

### Multi-table Inheritance

This approach is based
on [Multi-table Inheritance](https://docs.djangoproject.com/en/3.2/topics/db/models/#multi-table-inheritance) and a
hierarchy of `conformity_check` tables. There's one concrete `conformity_check_*` table per referencable resource type.
The common attributes of a check reside in the base table, only the foreign keys are placed in the child tables.

![Model using multi-table inheritance](drawio_mrmap_polymorphic_fks-multi-table-inheritance.png)

### django-polymorphic

This approach looks very similar to the Mulit-table Inheritance approach, but
uses [django-polymorphic](https://django-polymorphic.readthedocs.io/en/stable/)
for the `ConformityCheck` model and it's child types. This comes with a number of benefits when using the model,
particularly it is possible to query the base `ConformityCheck` model, albeit retrieving instances of the specific
subclasses. In the relational model, a column `polymorphic_ctype_id` is added to the base table that references
the `django_content_type` table.

![Model using django-polymorphic](drawio_mrmap_polymorphic_fks-django-polymorphic.png)

## Observations


## Conclusion

The django application for reproducing the test scenario and performing the benchmarks can be
found [here](https://github.com/MrSnyder/django-orm-playground).