The Banff Processor is part of the Banff project. It is a tool that can be installed in addition to the Banff Procedure package. This tool is used to implement an imputation strategy, which is essentially a sequence of processing steps. A processing step can be a standard Banff Procedure, a user-defined process (plugin) or a process block (another sequence of processing steps). 

Imputation strategies are defined using XML files, an Excel template has been provided along with a utility to convert metadata created with the template to the XML files required by the processor. The output of a processor job is the imputed file along with a log and various status and optional diagnostic files.

## Project Overview

The Banff Processor was originally written in SAS 9 using the SAS macro language. In 2023-24, the Banff Processor was redeveloped as a python package and released as version 2. New features were added such as Process Controls and Process Blocks.

