
def build_configargparser(parser):
    parser.add_argument("--iws_file", type=str, required=True)
    parser.add_argument("--labelmap_with_catheter_meshes_f", type=str, required=True)
    parser.add_argument("--labelmap_aorta_catheter", type=str, required=True)
    parser.add_argument("--save_dir_us_sim", type=str, required=True)
    parser.add_argument("--save_dir_us_sim_imgs", default="imgs/", type=str, required=True)
    parser.add_argument("--save_dir_us_sim_masks", default="masks/", type=str, required=True)
    parser.add_argument("--splines_file", type=str, required=True)
    parser.add_argument("--folder_catheter_data_path", type=str, required=True)

    parser.add_argument("--nr_imgs", default=100, type=int, required=False)
    parser.add_argument("--nr_labelmap", default=100, type=int, required=False)

    known_args, _ = parser.parse_known_args()
    return parser, known_args




#     opt, _ = parser.parse_known_args()
#     return parser
# known_args, _ = parser.parse_known_args()
# return parser, known_args