/*
   Unix SMB/CIFS implementation.

   libndr compression support

   Copyright (C) Stefan Metzmacher 2005
   Copyright (C) Matthieu Suiche 2008

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef __LIBRPC_NDR_NDR_COMPRESSION_H__
#define __LIBRPC_NDR_NDR_COMPRESSION_H__

#undef _PRINTF_ATTRIBUTE
#define _PRINTF_ATTRIBUTE(a1, a2) PRINTF_ATTRIBUTE(a1, a2)

/* this file contains prototypes for functions that are private 
 * to this subsystem or library. These functions should not be 
 * used outside this particular subsystem! */

/* The following definitions come from librpc/ndr/ndr_compression.c  */

enum ndr_err_code ndr_pull_compression_start(struct ndr_pull *subndr,
				    struct ndr_pull **_comndr,
				    enum ndr_compression_alg compression_alg,
				    ssize_t decompressed_len,
				    ssize_t compressed_len);
enum ndr_err_code ndr_pull_compression_end(struct ndr_pull *subndr,
				  struct ndr_pull *comndr,
				  enum ndr_compression_alg compression_alg,
				  ssize_t decompressed_len);
enum ndr_err_code ndr_push_compression_start(struct ndr_push *subndr,
				    struct ndr_push **_uncomndr,
				    enum ndr_compression_alg compression_alg);
enum ndr_err_code ndr_push_compression_end(struct ndr_push *subndr,
				  struct ndr_push *uncomndr,
				  enum ndr_compression_alg compression_alg);

enum ndr_err_code ndr_pull_compression_state_init(struct ndr_pull *ndr,
						  enum ndr_compression_alg compression_alg,
						  struct ndr_compression_state **state);
void ndr_pull_compression_state_free(struct ndr_compression_state *state);
enum ndr_err_code ndr_push_compression_state_init(struct ndr_push *ndr,
						  enum ndr_compression_alg compression_alg,
						  struct ndr_compression_state **state);

#undef _PRINTF_ATTRIBUTE
#define _PRINTF_ATTRIBUTE(a1, a2)

#endif /* __LIBRPC_NDR_NDR_COMPRESSION_H__ */

