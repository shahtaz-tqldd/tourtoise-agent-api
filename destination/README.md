-- Function to get complete destination data
CREATE OR REPLACE FUNCTION get_destination_complete(dest_id UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'id', d.id,
        'name', d.name,
        'location', json_build_object(
            'region', d.region,
            'country', d.country,
            'long', d.longitude,
            'lat', d.latitude
        ),
        'description', d.description,
        'images', (
            SELECT json_agg(image_url ORDER BY display_order)
            FROM destination_images WHERE destination_id = d.id
        ),
        'tags', (
            SELECT json_agg(tag_name)
            FROM destination_tags WHERE destination_id = d.id
        ),
        'highlights', (
            SELECT json_build_object(
                'best_time', best_time,
                'cost_level', cost_level,
                'avg_duration', avg_duration,
                'suitable_for', suitable_for,
                'popular_for', popular_for
            )
            FROM destination_highlights WHERE destination_id = d.id
        ),
        'stays', (
            SELECT json_build_object(
                'types', (
                    SELECT json_agg(json_build_object(
                        'category', category,
                        'description', description,
                        'price_range', price_range
                    ) ORDER BY display_order)
                    FROM stay_types WHERE destination_id = d.id
                ),
                'suggested', (
                    SELECT json_agg(json_build_object(
                        'name', name,
                        'price_range', price_range,
                        'rating', rating,
                        'distance', distance
                    ) ORDER BY display_order)
                    FROM suggested_stays WHERE destination_id = d.id
                )
            )
        ),
        'attractions', (
            SELECT json_agg(json_build_object(
                'name', name,
                'distance', distance,
                'description', description,
                'tag', tag,
                'image_url', image_url
            ) ORDER BY display_order)
            FROM attractions WHERE destination_id = d.id
        ),
        'transportation', (
            SELECT json_build_object(
                'how_to_reach', (
                    SELECT how_to_reach 
                    FROM destination_transport_info 
                    WHERE destination_id = d.id
                ),
                'local_options', (
                    SELECT json_agg(json_build_object(
                        'type', transport_type,
                        'price_range', price_range
                    ) ORDER BY display_order)
                    FROM transportation_options WHERE destination_id = d.id
                )
            )
        ),
        'cuisine', (
            SELECT json_build_object(
                'signature', (
                    SELECT json_agg(json_build_object(
                        'name', name,
                        'tags', tags,
                        'is_recommended', is_recommended
                    ) ORDER BY display_order)
                    FROM signature_dishes WHERE destination_id = d.id
                ),
                'restaurants', (
                    SELECT json_agg(json_build_object(
                        'name', name,
                        'signature_dish', signature_dishes,
                        'rating', rating,
                        'location', json_build_object(
                            'area', area,
                            'long', longitude,
                            'lat', latitude
                        )
                    ) ORDER BY display_order)
                    FROM restaurants WHERE destination_id = d.id
                )
            )
        ),
        'activities', (
            SELECT json_agg(json_build_object(
                'name', name,
                'price_range', price_range
            ) ORDER BY display_order)
            FROM activities WHERE destination_id = d.id
        ),
        'visit_info', (
            SELECT json_build_object(
                'weather', weather,
                'peak_season', peak_season,
                'festivals', festivals
            )
            FROM visit_info WHERE destination_id = d.id
        ),
        'practical_info', (
            SELECT json_build_object(
                'languages', languages,
                'payment', payment_methods,
                'safety', safety_tips,
                'customs', customs
            )
            FROM practical_info WHERE destination_id = d.id
        )
    ) INTO result
    FROM destinations d
    WHERE d.id = dest_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;