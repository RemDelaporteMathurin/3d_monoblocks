from convert_mesh import convert_med_to_xdmf

for thickness in [4, 5, 6, 7, 8, 9, 10, 14]:
    print('Converting thickness {} mm'.format(thickness))
    folder = "{}mm_thickness".format(thickness)
    correspondance_dict, cell_data_types = convert_med_to_xdmf(
        medfilename="{}/mesh_3D_{}mm_no_gap.med".format(folder, thickness),
        cell_file="{}/mesh_cells_no_gap.xdmf".format(folder),
        facet_file="{}/mesh_facets_no_gap.xdmf".format(folder),
        cell_type="tetra",
        facet_type="triangle",
    )

print(correspondance_dict)
